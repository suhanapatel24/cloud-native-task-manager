import pytest
from app import create_app, db

@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def test_health(client):
    assert client.get("/healthz").status_code == 200

def test_task_crud(client):
    created = client.post("/api/tasks", json={"title": "Learn Kubernetes", "priority": "high"})
    assert created.status_code == 201
    task = created.get_json()
    task_id = task["id"]

    assert client.get(f"/api/tasks/{task_id}").status_code == 200

    updated = client.patch(f"/api/tasks/{task_id}", json={"completed": True})
    assert updated.get_json()["completed"] is True

    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404

def test_validation(client):
    assert client.post("/api/tasks", json={}).status_code == 400
    assert client.post("/api/tasks", json={"title": "x", "priority": "urgent"}).status_code == 400
