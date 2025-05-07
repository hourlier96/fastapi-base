from typing import List

from pydantic import BaseModel, ConfigDict

from .todo import TodoRead


class UserBase(BaseModel):
    email: str


class UserRead(UserBase):
    id: int
    todos: List[TodoRead] = []

    # Ensure Pydantic can populate 'UserRead' schema from 'User' model
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass
