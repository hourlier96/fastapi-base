from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .todo import Todo

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    todos: Mapped[List["Todo"]] = relationship(back_populates="user")
