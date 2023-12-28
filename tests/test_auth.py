from src.main import app
from fastapi.testclient import TestClient
from src.config import settings
import pytest


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user():
    email = settings.TEST_VALID_EMAIL
    fullname = settings.TEST_VALID_FULLNAME
    return {"email": email, "fullname": fullname}


def test_login(client, test_user):
    login_res = client.post("/login/", json=test_user)
    assert login_res.status_code == 200
    json_token = login_res.json()["access_token"]
    assert json_token is not None
    return json_token
