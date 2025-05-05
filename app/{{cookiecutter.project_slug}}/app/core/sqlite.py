from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
session = Session(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]