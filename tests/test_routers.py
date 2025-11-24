from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
def test_image_path():
    return Path("tests/assets/test.png")

@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_vector_editor():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/vector")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_upload_file(test_image_path):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with open(test_image_path, "rb") as f:
            response = await ac.post("/upload", files={"file": f})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_resize_image(test_image_path):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with open(test_image_path, "rb") as f:
            response = await ac.post("/upload", files={"file": f})
        image_id = response.text.split('value="')[1].split('"')[0]
        response = await ac.post("/resize", data={"width": 50, "height": 50, "image_id": image_id})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_download_image(test_image_path):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with open(test_image_path, "rb") as f:
            response = await ac.post("/upload", files={"file": f})
        image_id = response.text.split('value="')[1].split('"')[0]
        response = await ac.post("/download", data={"image_id": image_id, "format": "png"})
    assert response.status_code == 200
