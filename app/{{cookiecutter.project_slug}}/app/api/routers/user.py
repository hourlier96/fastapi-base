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