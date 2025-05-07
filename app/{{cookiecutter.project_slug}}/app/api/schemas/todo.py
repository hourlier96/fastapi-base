from enum import Enum

from pydantic import BaseModel, ConfigDict


class TodoStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TodoBase(BaseModel):
    title: str
    status: TodoStatus


class TodoRead(TodoBase):
    id: int

    # Ensure Pydantic can populate 'TodoRead' schema from 'Todo' model
    model_config = ConfigDict(from_attributes=True)


class TodoReadWithUser(TodoBase):
    user_id: int


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass
