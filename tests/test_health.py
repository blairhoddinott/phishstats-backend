from httpx import ASGITransport, AsyncClient

from app.main import app


async def test_root() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to phishstats-backend"


async def test_healthcheck() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
