import reflex as rx

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
                spacing="6",
            ),
            justify="between",
            align="center",
            width="100%",
            padding="1em 2em",
        ),
        background="#1a1a2e",
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 8px rgba(0,0,0,0.3)",
    )