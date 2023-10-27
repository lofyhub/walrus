from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

auth_token = "fake_token_here"


def test_post_business():
    response = client.post(
        "/businesses/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid or expired token"}
