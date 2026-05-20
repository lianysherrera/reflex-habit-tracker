from typing import Optional
from sqlmodel import Field, sqlModel

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    emoji: str = "✅"