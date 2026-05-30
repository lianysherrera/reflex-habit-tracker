import reflex as rx
from pydantic import BaseModel
from sqlmodel import select
from datetime import date, timedelta
from reflex_habit_tracker.models import Habit, HabitLog
from reflex_habit_tracker.navbar import navbar


class HabitItem(BaseModel):
    id: int = 0
    name: str = ""
    emoji: str = ""
    streak: int = 0 #racha de días consecutivos
    percentage: int = 0
    completed_today: bool = False

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
            today = date.today()
            
            completed_logs = session.exec(
                select(HabitLog).where(HabitLog.log_date == today)
            ).all()
            completed_ids = [log.habit_id for log in completed_logs]

            self.habits = [
                HabitItem(
                    id=h.id or 0,
                    name=h.name,
                    emoji=h.emoji,
                    streak=self.get_streak(h.id, session),
                    percentage=self.get_percentage(h.id, session),
                    completed_today=(h.id in completed_ids),
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
        rx.table.cell(
            rx.hstack(
                rx.text(habit.emoji, font_size="1.2em"),
                rx.text(
                    habit.name,
                    color=rx.cond(habit.completed_today, "var(--gray-9)", "inherit"),
                    text_decoration=rx.cond(habit.completed_today, "line-through", "none"),
                ),
                spacing="2",
                align="center",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.text(
                    habit.streak.to_string(),
                    font_weight="500",
                    color="var(--gray-12)",
                ),
                rx.text("días", color="var(--gray-9)", font_size="0.85em"),
                spacing="1",
                align="center",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.progress(
                    value=habit.percentage,
                    width="72px",
                    height="4px",
                    color_scheme="blue",
                ),
                rx.text(
                    habit.percentage.to_string() + "%",
                    color="var(--gray-9)",
                    font_size="0.8em",
                    width="36px",
                ),
                spacing="2",
                align="center",
            )
        ),
        rx.table.cell(
            rx.cond(
                habit.completed_today,
                rx.icon("circle-check", color="var(--green-9)", size=18),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("check", size=14),
                        on_click=HabitsPageState.complete_habit(habit.id),
                        color_scheme="gray",
                        variant="ghost",
                        size="1",
                        cursor="pointer",
                    ),
                    rx.icon_button(
                        rx.icon("trash-2", size=14),
                        on_click=HabitsPageState.delete_habit(habit.id),
                        color_scheme="gray",
                        variant="ghost",
                        size="1",
                        cursor="pointer",
                    ),
                    spacing="4",
                ),
            ),
        ),
    )


def habits_page():
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.toast.provider(),
                rx.heading(
                    "Mis Habitos",
                    font_size="1.6em",
                    font_weight="500",
                    color="var(--gray-12)",
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                "Habito",
                                color="white",
                                font_size="1em",
                                font_weight="600",
                                text_transform="uppercase",
                                letter_spacing="0.05em",
                            ),
                            rx.table.column_header_cell(
                                "Racha",
                                color="white",
                                font_size="1em",
                                font_weight="600",
                                text_transform="uppercase",
                                letter_spacing="0.05em",
                            ),
                            rx.table.column_header_cell(
                                "Esta semana",
                                color="white",
                                font_size="1em",
                                font_weight="600",
                                text_transform="uppercase",
                                letter_spacing="0.05em",
                            ),
                            rx.table.column_header_cell(""),
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
        ),
    )