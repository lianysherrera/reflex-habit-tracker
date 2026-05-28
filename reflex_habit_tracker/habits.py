import reflex as rx
from pydantic import BaseModel
from sqlmodel import select
from reflex_habit_tracker.models import Habit
from reflex_habit_tracker.navbar import navbar


class HabitItem(BaseModel):
    id: int = 0
    name: str = ""
    emoji: str = ""


class HabitState(rx.State):
    name: str = ""
    emoji: str = ""

    def set_name(self, value: str):
        self.name = value

    def set_emoji(self, value: str):
        self.emoji = value

    def add_habit(self):
        if self.name.strip() == "":
            return

        with rx.session() as session:
            session.add(Habit(
                name=self.name,
                emoji=self.emoji if self.emoji.strip() != "" else "✅",
            ))
            session.commit()

        self.name = ""
        self.emoji = ""
        return rx.toast.success("Habito creado!")


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
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.toast.provider(),
                rx.heading("Tracker de Habitos", font_size="2.5em"),
                rx.text("Construye habitos, cambia tu vida", color="gray"),
                rx.divider(),
                habit_form(),
                align="center",
                spacing="6",
                padding="2em",
            ),
            min_height="100vh",
        ),
    )