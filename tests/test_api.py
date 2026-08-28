import os
import tempfile

TEST_DB = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
os.environ["DEV_DESK_DB"] = TEST_DB

from fastapi.testclient import TestClient
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
        assert client.get("/tasks", headers=headers).json()[0]["title"] == "Ship DevDesk"
        assert client.patch(f"/tasks/{task_id}", headers=headers, json={"completed": True}).json()["completed"] is True
        assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 200
        client.post("/auth/logout", headers=headers)


# The test database is isolated from the developer's local database.
import pathlib
pathlib.Path(TEST_DB).unlink(missing_ok=True)
