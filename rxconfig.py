import reflex as rx

config = rx.Config(
    app_name="reflex_habit_tracker",
    db_url="sqlite:///habits.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)