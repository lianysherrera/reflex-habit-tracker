import reflex as rx
from reflex_habit_tracker.styles import PRIMARY, ACCENT

def navbar():
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("Tracker de Habitos", font_size="1.2em", color="white"),
                href="/",
                text_decoration="none",
            ),
            rx.hstack(
                rx.link(
                    "Inicio",
                    href="/",
                    color="white",
                    text_decoration="none",
                    _hover={"color": "#a78bfa"},
                ),
                rx.link(
                    "Mis Hábitos",
                    href="/habits",
                    color="white",
                    text_decoration="none",
                    _hover={"color": "#a78bfa"},
                ),
                rx.link(
                    "Estadisticas",
                    href="/stats",
                    color=ACCENT,
                    text_decoration="none",
                    _hover={"color": "#a78bfa"},
                ),
                spacing="6",
            ),
            justify="between",
            align="center",
            width="100%",
            padding="1em 2em",
        ),
        background="trasnparent",
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 8px rgba(0,0,0,0.3)",
        border_bottom="1px solid white",
    )