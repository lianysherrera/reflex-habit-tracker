import reflex as rx
from reflex_habit_tracker.habits import index

app = rx.App()
app.add_page(index, route="/")