import pytest
from app import create_app, db_manager


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    with app.app_context():
        yield app.test_client()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert "db" in data["components"]
    assert data["components"]["db"]["status"] == "UP"


def test_get_books_unauthorized(client):
    response = client.get("/api/v1/books")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"]["code"] == 4010001
    assert "Unauthorized" in data["error"]["message"]


def test_get_books(client):
    response = client.get("/api/v1/books", headers={"Authorization": "Basic bWU6bWU="})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]
    assert "author" in data[0]
