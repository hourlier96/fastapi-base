from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.sqlite import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    todos: Mapped[List["Todo"]] = relationship(back_populates="user")
