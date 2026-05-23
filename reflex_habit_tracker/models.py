from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    emoji: str = "✅"

#Modelo de registro diario
class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int  = Field(foreign_key="habit.id")
    log_date: date = Field(default_factory=date.today)