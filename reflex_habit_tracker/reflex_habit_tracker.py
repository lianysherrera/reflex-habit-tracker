import reflex as rx
from reflex_habit_tracker.habits import index
from reflex_habit_tracker import models

app = rx.App()
app.add_page(index, route="/")