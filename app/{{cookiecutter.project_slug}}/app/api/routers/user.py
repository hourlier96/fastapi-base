from typing import Dict, Annotated
from fastapi import APIRouter, Depends, Query

{% if cookiecutter.database == "mongodb (motor)" -%}
from app.core.mongodb import SessionDep

router = APIRouter()

@router.get("")
async def get_user_by_email(email: Annotated[str, Query()], session: SessionDep) -> Dict:
    query_filter = {
        "email": email
    }
    cursor = await session.find("test_collection", query_filter, multiple=True)
    response = await cursor.to_list()
    for e in response:
        e["_id"] = str(e["_id"])
    return {"users": response}

@router.post("")
async def create_user(user: Dict, session: SessionDep) -> Dict:
    await session.insert("test_collection", user)
    return {"status": "User created"}
{% endif %}

{% if cookiecutter.database == "sqlite (aiosqlite)" -%}
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.sqlite import SessionDep
from app.api.deps import raise_400, raise_404, raise_500
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDep) -> UserRead:
    stmt = select(User).where(User.id == user_id).options(selectinload(User.todos))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise_404(msg=f"User with id {user_id} not found")
    return user


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(user_in: UserCreate, session: SessionDep):
    stmt = select(User).where(User.email == user_in.email)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise_400(msg='Email already registered')

    user_obj = User(email=user_in.email)
    session.add(user_obj)

    try:
        await session.commit()
        await session.refresh(user_obj)
    except Exception as e:
        await session.rollback()
        raise_500()

{% endif %}