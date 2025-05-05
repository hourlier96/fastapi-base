from enum import Enum
from pydantic import BaseModel


class TodoStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TodoCreate(BaseModel):
    title: str
    status: TodoStatus
    user_id: int


class TodoRead(TodoCreate):
    id: int


class TodoUpdate(TodoCreate):
    pass
