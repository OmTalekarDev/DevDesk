import os
import tempfile

os.environ["DEV_DESK_TESTING"] = "1"

from fastapi.testclient import TestClient

from app.database import DATABASE_PATH
from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_register_and_task_crud():
    with TestClient(app) as client:
        username = "test_user_123"
        register = client.post("/auth/register", json={"username": username, "password": "password123"})
        assert register.status_code == 201
        token = register.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        created = client.post("/tasks", headers=headers, json={"title": "Ship DevDesk", "description": "Finish v2"})
        assert created.status_code == 201
        task_id = created.json()["id"]

        listed = client.get("/tasks", headers=headers)
        assert listed.status_code == 200
        assert listed.json()[0]["title"] == "Ship DevDesk"

        updated = client.patch(f"/tasks/{task_id}", headers=headers, json={"completed": True})
        assert updated.status_code == 200
        assert updated.json()["completed"] is True

        deleted = client.delete(f"/tasks/{task_id}", headers=headers)
        assert deleted.status_code == 200

        client.post("/auth/logout", headers=headers)

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
