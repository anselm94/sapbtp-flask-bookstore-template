import pytest
from app.utils.heathcheck_utils import run_health_check
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


def test_run_health_check(app):
    result = run_health_check(app.config)
    assert result["status"] == "UP"
    assert "db" in result["components"]
    assert result["components"]["db"]["status"] == "UP"
