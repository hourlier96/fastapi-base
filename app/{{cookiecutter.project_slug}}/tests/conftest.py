from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac
