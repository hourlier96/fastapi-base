from contextlib import ExitStack
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app as actual_app


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app


@pytest_asyncio.fixture(scope="function")  # <--- Change decorator here
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac
