import reflex as rx
from pydantic import BaseModel
from sqlmodel import select
from datetime import date, timedelta
from reflex_habit_tracker.models import Habit, HabitLog


class HabitItem(BaseModel):
    id: int = 0
    name: str = ""
    emoji: str = ""
    streak: int = 0 #racha de días consecutivos
    percentage: int = 0

class HabitsPageState(rx.State):
    habits: list[HabitItem] = []

    def get_streak(self, habit_id: int, session) -> int:
        logs = session.exec(
            select(HabitLog)
            .where(HabitLog.habit_id == habit_id)
            .order_by(HabitLog.log_date.desc())
        ).all()

        if not logs:
            return 0

        streak = 0
        check_date = date.today()

        for log in logs:
            if log.log_date == check_date:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        return streak

    def get_percentage(self, habit_id: int, session) -> int:
        today = date.today()
        week_ago = today - timedelta(days=7)

        logs = session.exec(
            select(HabitLog).where(
                HabitLog.habit_id == habit_id,
                HabitLog.log_date >= week_ago,
                HabitLog.log_date <= today,
            )
        ).all()
        return int(len(logs) / 7 * 100)

        
    def load_habits(self):
        with rx.session() as session:
            db_habits = session.exec(select(Habit)).all()
            self.habits = [
                HabitItem(
                    id=h.id or 0,
                    name=h.name,
                    emoji=h.emoji,
                    streak=self.get_streak(h.id, session),
                    percentage=self.get_percentage(h.id, session),
                )
                for h in db_habits
            ]

    def complete_habit(self, habit_id: int):
        with rx.session() as session:

            existing = session.exec(
                select(HabitLog).where(
                    HabitLog.habit_id == habit_id,
                    HabitLog.log_date == date.today(),
                )
            ).first()

            if existing:
                return rx.toast.error("Ya completaste este habito hoy!")
                
            session.add(HabitLog(
                habit_id=habit_id,
                log_date=date.today(),
            ))
            session.commit()
        return rx.toast.success("Habito completado hoy!")

    def delete_habit(self, habit_id: int):
        with rx.session() as session:
            habit = session.exec(
                select(Habit).where(Habit.id == habit_id)
            ).first()
            if habit:
                session.delete(habit)
                session.commit()
        self.load_habits()
        return rx.toast.success("Habito eliminado!")


def habit_row(habit: HabitItem):
    return rx.table.row(
        rx.table.cell(habit.emoji),
        rx.table.cell(habit.name),
        rx.table.cell(
            rx.hstack(
                rx.text(habit.streak.to_string()),
                rx.text("dias"),
                spacing="1",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.progress(value=habit.percentage, width="80px"),
                rx.text(habit.percentage.to_string()),
                rx.text("%"),
                spacing="1",
                align="center",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Completado",
                    on_click=HabitsPageState.complete_habit(habit.id),
                    color_scheme="green",
                    size="1",
                ),
                rx.button(
                    "Eliminar",
                    on_click=HabitsPageState.delete_habit(habit.id),
                    color_scheme="red",
                    variant="ghost",
                    size="1",
                ),
                spacing="2",
            )
        ),
    )



def habits_page():
    return rx.center(
        rx.vstack(
            rx.toast.provider(),
            rx.heading("Mis Habitos", font_size="2em"),
            rx.link(
                rx.button(" <- Volver", variant="ghost"),
                href="/",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(""),
                        rx.table.column_header_cell("Habito"),
                        rx.table.column_header_cell("Racha"),
                        rx.table.column_header_cell("Esta semana"),
                        rx.table.column_header_cell("Acciones"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        HabitsPageState.habits,
                        habit_row,
                    ),
                ),
                width="600px",
            ),
            align="center",
            spacing="5",
            padding="2em",
            on_mount=HabitsPageState.load_habits,
        ),
        min_height="100vh",
    )