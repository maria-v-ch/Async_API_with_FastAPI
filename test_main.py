import pytest
from httpx import AsyncClient
from main import app
import asyncio


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/task", json={"duration": 2})
        assert response.status_code == 200
        assert "task_id" in response.json()


@pytest.mark.asyncio
async def test_task_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a task
        response = await ac.post("/task", json={"duration": 2})
        task_id = response.json()["task_id"]

        # Check status immediately, should be running
        response = await ac.get(f"/task/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"status": "running"}

        # Wait for 3 seconds (more than task duration) to ensure the task is completed
        await asyncio.sleep(3)

        # Check status again, should be done
        response = await ac.get(f"/task/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"status": "done"}


@pytest.mark.asyncio
async def test_task_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/task/nonexistent_task_id")
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}
