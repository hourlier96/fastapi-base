from enum import Enum
from typing import List
from pydantic import BaseModel

from .todo import TodoRead


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    todos: List[TodoRead] = []

    class Config:
        orm_mode = True
