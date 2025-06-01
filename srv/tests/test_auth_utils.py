import pytest
from werkzeug.exceptions import Forbidden

from flask import Flask
from flask_login import LoginManager, login_user, logout_user

from app.utils.auth_utils import roles_required
from app.models import BaseUser, XsuaaUser, BasicUser


class DummyUser(BaseUser):
    def __init__(self, scopes):
        self._scopes = scopes
        self.id = "dummy_user"

    def check_scope(self, scope):
        return scope in self._scopes


class DummyRequest:
    def __init__(self, headers):
        self.headers = headers


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test"
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return DummyUser(["uaa.resource"])

    return app


def test_get_xsuaauser_from_request(monkeypatch):
    from app.utils import auth_utils

    class DummyXssecContext:
        pass

    app_config = {
        "AUTH_XSUAA_CRED": "dummy_cred",
    }

    # Patch `xssec` to return a dummy security context
    monkeypatch.setattr(
        auth_utils,
        "xssec",
        type(
            "xssec",
            (),
            {"create_security_context": lambda token, cred: DummyXssecContext()},
        ),
    )

    # Valid Bearer token
    req = DummyRequest({"authorization": "Bearer sometoken"})
    user = auth_utils.get_xsuaauser_from_request(app_config, req)
    assert isinstance(user, XsuaaUser)

    # No Bearer token
    req = DummyRequest({"authorization": None})
    assert auth_utils.get_xsuaauser_from_request(app_config, req) is None

    # Wrong header
    req = DummyRequest({"authorization": "Basic sometoken"})
    assert auth_utils.get_xsuaauser_from_request(app_config, req) is None


def test_get_basicuser_from_request():
    from app.utils import auth_utils
    import base64

    app_config = {
        "AUTH_USERS": {
            "foo": {"password": "bar"},
            "me": {"password": "me", "roles": ["uaa.resource"], "attr": {}},
        }
    }

    # Valid Basic Auth
    creds = base64.b64encode(b"foo:bar").decode()
    req = DummyRequest({"authorization": f"Basic {creds}"})
    user = auth_utils.get_basicuser_from_request(app_config, req)
    assert isinstance(user, BasicUser)

    # Invalid password
    creds = base64.b64encode(b"foo:wrong").decode()
    req = DummyRequest({"authorization": f"Basic {creds}"})
    assert auth_utils.get_basicuser_from_request(app_config, req) is None

    # No header
    req = DummyRequest({"authorization": None})
    assert auth_utils.get_basicuser_from_request(app_config, req) is None

    # Malformed header
    req = DummyRequest({"authorization": "Basic notbase64"})
    assert auth_utils.get_basicuser_from_request(app_config, req) is None

    # Missing username/password
    creds = base64.b64encode(b":").decode()
    req = DummyRequest({"authorization": f"Basic {creds}"})
    assert auth_utils.get_basicuser_from_request(app_config, req) is None


def test_roles_required_allows_access(app):
    @roles_required(["uaa.resource"])
    def protected():
        return "allowed"

    with app.test_request_context():
        login_user(DummyUser(["uaa.resource"]))
        assert protected() == "allowed"
        logout_user()


def test_roles_required_denies_access(app):
    @roles_required(["uaa.resource"])
    def protected():
        return "denied"

    with app.test_request_context():
        login_user(DummyUser([]))
        with pytest.raises(Exception) as excinfo:
            protected()

        assert isinstance(excinfo.value, Forbidden)
        assert "You do not have one or all roles required" in str(excinfo.value)
        logout_user()
