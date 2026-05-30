import reflex as rx
from reflex_habit_tracker.habits import index
from reflex_habit_tracker.habits_page import habits_page
from reflex_habit_tracker.stats import stats_page
from reflex_habit_tracker import models

app = rx.App()
app.add_page(index, route="/")
app.add_page(habits_page, route="/habits")
app.add_page(stats_page, route="/stats")