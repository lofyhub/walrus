from src.main import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user():
    return {"email": "johnphiliyui9@gmail.com", "fullname": "John Philip"}


def test_login(client, test_user):
    login_res = client.post("/login/", json=test_user)
    assert login_res.status_code == 200
    json_token = login_res.json()["access_token"]
    assert json_token is not None
    return json_token
