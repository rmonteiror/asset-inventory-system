import asyncio

import pytest
from httpx import AsyncClient

from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_asset():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/assets/",
            json={
                "name": "Laptop A",
                "serial_number": "SN12345",
                "category": "Laptop",
                "location": "Office",
                "notes": "Test asset",
            },
        )
        assert response.status_code == 201
        asset = response.json()
        assert asset["id"]
        assert asset["serial_number"] == "SN12345"

        get_response = await client.get(f"/api/assets/{asset['id']}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Laptop A"
