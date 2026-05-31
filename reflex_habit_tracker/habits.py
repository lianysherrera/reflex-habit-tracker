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
    return rx.vstack(
        rx.text(
            "Nuevo habito",
            font_size="0.78em",
            font_weight="600",
            letter_spacing="0.08em",
            text_transform="uppercase",
            color="var(--gray-9)",
        ),
        rx.hstack(
            rx.input(
                placeholder="✦",
                on_change=HabitState.set_emoji,
                value=HabitState.emoji,
                width="56px",
                text_align="center",
                font_size="1.1em",
                border="1.5px solid var(--gray-5)",
                border_radius="10px",
                background="transparent",
                flex_shrink="0",
            ),
            rx.input(
                placeholder="¿Qué habito quieres crear?",
                on_change=HabitState.set_name,
                value=HabitState.name,
                flex="1",
                border="1.5px solid var(--gray-5)",
                border_radius="10px",
                background="transparent",
                font_size="0.95em",
            ),
            spacing="2",
            width="100%",
        ),
        rx.button(
            "Añadir habito",
            on_click=HabitState.add_habit,
            width="100%",
            border_radius="10px",
            font_weight="500",
            font_size="0.95em",
            height="42px",
            background="var(--gray-12)",
            color="var(--gray-1)",
            cursor="pointer",
        ),
        spacing="3",
        width="100%",
    )



def index():
    return rx.box(
        navbar(),
        rx.toast.provider(),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading(
                        "Tracker de Habitos",
                        font_size="2.2em",
                        font_weight="700",
                        letter_spacing="-0.03em",
                        color="var(--gray-12)",
                    ),
                    rx.text(
                        "Construye habitos, cambia tu vida",
                        font_size="0.95em",
                        color="var(--gray-9)",
                    ),
                    align="center",
                    spacing="1",
                ),
                rx.box(height="0.5em"),
                habit_form(),
                align="stretch",
                spacing="3",
                width="380px",
                padding="3em 0",
            ),
            min_height="100vh",
            background="var(--gray-1)",
        ),
    )