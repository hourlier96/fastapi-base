from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app as actual_app


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=actual_app)
    async with AsyncClient(transport=transport, base_url="http://fakeurl") as ac:
        yield ac
