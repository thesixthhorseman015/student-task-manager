import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    tasks.clear()
    with app.test_client() as client:
        yield client
    tasks.clear()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Task Manager" in response.data

def test_add_task(client):
    response = client.post(
        "/add",
        data={"title": "Complete DevOps assignment", "deadline": "2026-10-20"}
    )
    assert response.status_code == 302
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Complete DevOps assignment"

def test_empty_title_rejected(client):
    response = client.post("/add", data={"title": "   "})
    assert response.status_code == 400
    assert len(tasks) == 0