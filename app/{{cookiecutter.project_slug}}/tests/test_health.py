import pytest
from httpx import AsyncClient

from app.core.config import settings

DATASOURCES_URL = f"{settings.API_PREFIX}/health"


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.head(
        DATASOURCES_URL,
    )
    assert response.status_code == 200
