import reflex as rx
from pydantic import BaseModel
from sqlmodel import select
from reflex_habit_tracker.models import Habit


# Modelo serializable para el State
# Nunca meter SQLModel con table=True en el State
class HabitItem(BaseModel):
    id: int = 0
    name: str = ""
    emoji: str = ""


class HabitState(rx.State):
    name: str = ""
    emoji: str = ""
    habits: list[HabitItem] = []

    def set_name(self, value: str):
        self.name = value

    def set_emoji(self, value: str):
        self.emoji = value

    def load_habits(self):
        with rx.session() as session:
            db_habits = session.exec(select(Habit)).all()
            self.habits = [
                HabitItem(id=h.id or 0, name=h.name, emoji=h.emoji)
                for h in db_habits
            ]

    def add_habit(self):
        if self.name.strip() == "":
            return

        # Guarda en la BD
        with rx.session() as session:
            session.add(Habit(
                name=self.name,
                emoji=self.emoji if self.emoji.strip() != "" else "✅",
            ))
            session.commit()

        self.name = ""
        self.emoji = ""
        self.load_habits()

    def delete_habit(self, habit_id: int):
        with rx.session() as session:
            habit = session.exec(
                select(Habit).where(Habit.id == habit_id)
            ).first()
            if habit:
                session.delete(habit)
                session.commit()
        self.load_habits()


def habit_card(habit: HabitItem):
    return rx.box(
        rx.hstack(
            rx.text(habit.emoji, font_size="1.5em"),
            rx.text(habit.name, font_size="1.1em"),
            rx.spacer(),
            rx.button(
                "Eliminar",
                on_click=HabitState.delete_habit(habit.id),
                color_scheme="red",
                variant="ghost",
                size="1",
            ),
            align="center",
            width="100%",
        ),
        border="1px solid #e2e8f0",
        border_radius="8px",
        padding="1em",
        width="300px",
    )


def habit_form():
    return rx.box(
        rx.vstack(
            rx.heading("Nuevo habito", font_size="1.5em"),
            rx.input(
                placeholder="Nombre del habito...",
                on_change=HabitState.set_name,
                value=HabitState.name,
                width="300px",
            ),
            rx.input(
                placeholder="Emoji...",
                on_change=HabitState.set_emoji,
                value=HabitState.emoji,
                width="300px",
            ),
            rx.button(
                "Añadir habito",
                on_click=HabitState.add_habit,
                color_scheme="green",
                width="300px",
            ),
            align="center",
            spacing="3",
        ),
        border="1px solid #e2e8f0",
        border_radius="8px",
        padding="2em",
    )


def index():
    return rx.center(
        rx.vstack(
            rx.heading("Tracker de Habitos", font_size="2.5em"),
            rx.text("Construye habitos, cambia tu vida", color="gray"),
            rx.divider(),
            habit_form(),
            rx.divider(),
            rx.heading("Mis habitos", font_size="1.5em"),
            rx.vstack(
                rx.foreach(
                    HabitState.habits,
                    habit_card,
                ),
                spacing="3",
            ),
            align="center",
            spacing="6",
            padding="2em",
            on_mount=HabitState.load_habits,
        ),
        min_height="100vh",
    )