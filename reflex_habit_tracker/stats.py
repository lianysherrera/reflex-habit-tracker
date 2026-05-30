import reflex as rx
from pydantic import BaseModel
from sqlmodel import select
from datetime import date, timedelta
from reflex_habit_tracker.models import Habit, HabitLog
from reflex_habit_tracker.navbar import navbar

class StatsData(BaseModel):
    completed_today: int = 0
    pending_today: int = 0
    best_streak_name: str = ""
    best_streak_count: int = 0
    best_percentage_name: str = ""
    best_percentage_count: int = 0
    total_this_week: int = 0

class StatsState(rx.State):
    stats: StatsData = StatsData()
    
    def load_stats(self):
        with rx.session() as session:
            habits = session.exec(select(Habit)).all()
            today = date.today()
            week_ago = today - timedelta(days=7)

            # habitos completados hoy
            completed_today = session.exec(
                select(HabitLog).where(
                    HabitLog.log_date == today
                )
            ).all()
            completed_ids = [log.habit_id for log in completed_today]

            # pendientes hoy
            pending_today = len ([h for h in habits if h.id not in completed_ids])

            # total esta semana
            total_week = session.exec(
                select(HabitLog).where(
                    HabitLog.log_date >= week_ago,
                    HabitLog.log_date <= today,
                )
            ).all()

            # mejor racha y mejor porcentaje
            best_streak_name = ""
            best_streak_count = 0
            best_percentage_name = ""
            best_percentage_count = 0

            for habit in habits:
                logs = session.exec(
                    select(HabitLog)
                    .where(HabitLog.habit_id == habit.id)
                    .order_by(HabitLog.log_date.desc())
                ).all()

                streak = 0
                check_date = today
                for log in logs:
                    if log.log_date == check_date:
                        streak += 1
                        check_date -= timedelta(days=1)
                    else:
                        break
                
                if streak > best_streak_count:
                    best_streak_count = streak
                    best_streak_name = habit.name
                
                # calcular porcentaje
                week_logs = session.exec(
                    select(HabitLog).where(
                        HabitLog.habit_id == habit.id,
                        HabitLog.log_date >= week_ago,
                        HabitLog.log_date <= today,
                    )
                ).all()

                percentage = int(len(week_logs) / 7 * 100)
                if percentage > best_percentage_count:
                    best_percentage_count = percentage
                    best_percentage_name = habit.name

            self.stats = StatsData(
                completed_today=len(completed_today),
                pending_today=pending_today,
                best_streak_name=best_streak_name,
                best_streak_count=best_streak_count,
                best_percentage_name=best_percentage_name,
                best_percentage_count=best_percentage_count,
                total_this_week=len(total_week),
            )


def stat_card(title: str, value: rx.Component, bg: str):
    return rx.box(
        rx.vstack(
            rx.text(title, color="white", font_size="0.9em"),
            value,
            align="center",
            spacing="2",
        ),
        background="transparent",
        border="1px solid white",
        border_radius="16px",
        padding="1.5em 2em",
        min_width="180px",
        text_align="center",
        margin="12px",
    )


def stats_page():
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Estadisticas", font_size="2em"),
                rx.divider(),
                rx.heading("Hoy", font_size="1.3em"),
                rx.flex(
                    stat_card(
                        "Completados hoy",
                        rx.heading(
                            StatsState.stats.completed_today.to_string(),
                            font_size="2em",
                            color="green",
                        ),
                        "#f0fdf4",
                    ),
                    stat_card(
                        "Pendientes hoy",
                        rx.heading(
                            StatsState.stats.pending_today.to_string(),
                            font_size="2em",
                            color="orange",
                        ),
                        "#fff7ed",
                    ),
                    stat_card(
                        "Total esta semana",
                        rx.heading(
                            StatsState.stats.total_this_week.to_string(),
                            font_size="2em",
                            color="blue",
                        ),
                        "#eff6ff",
                    ),
                    gap="6",
                    flex_wrap="wrap",
                    justify="center",
                ),
                rx.divider(),
                rx.heading("Mejores habitos", font_size="1.3em"),
                rx.flex(
                    stat_card(
                        "Mejor racha",
                        rx.vstack(
                            rx.heading(
                                StatsState.stats.best_streak_name,
                                font_size="1.2em",
                                color="purple",
                            ),
                            rx.text(
                                StatsState.stats.best_streak_count.to_string() + " dias",
                                color="purple",
                            ),
                            align="center",
                            spacing="1",
                        ),
                        "#faf5ff",
                    ),
                    stat_card(
                        "Mejor % semanal",
                        rx.vstack(
                            rx.heading(
                                StatsState.stats.best_percentage_name,
                                font_size="1.2em",
                                color="blue",
                            ),
                            rx.text(
                                StatsState.stats.best_percentage_count.to_string() + "%",
                                color="blue",
                            ),
                            align="center",
                            spacing="1",
                        ),
                        "#eff6ff",
                    ),
                    gap="6",
                    flex_wrap="wrap",
                    justify="center",
                ),
                align="center",
                spacing="5",
                padding="2em",
                on_mount=StatsState.load_stats,
            ),
            min_height="100vh",
        ),
    )