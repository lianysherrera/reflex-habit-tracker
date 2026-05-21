import reflex as rx

class HabitState(rx.State):
    name: str = ""
    emoji: str = ""

    def set_name(self, value: str):
        self.name = value
    
    def set_emoji(self, value: str):
        self.emoji = value

    def add_habit(self):
        # probar imprimir en consola
        print(f"Habito: {self.name}{self.emoji}")


def habit_form():
    return rx.box(
        rx.vstack(
            rx.heading("Nuevo habito", font_size="1.5em"),
            rx.input(
                placeholder="Nombre habito..",
                on_change=HabitState.set_name,
                value=HabitState.name,
                width="300px",
            ),
            rx.input(
                placeholder="Emoji..",
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
            align="center",
            spacing="6",
            padding="2em",
        ),
        min_height="100vh",
    )