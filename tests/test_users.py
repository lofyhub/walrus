from fastapi.testclient import TestClient
from .test_auth import client, test_login, test_user
from src.auth.auth import get_user_from_token
from src.config import settings


def test_add_user(client: TestClient, test_user: dict):
    test_data = {
        "email": "test_email@gmail.com",
        "fullname": "Test Name",
        "tel_number": settings.TEST_VALID_TEL_NUMBER,
        "picture": "https://images.pexels.com/photos/19561453/pexels-photo-19561453.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    }

    response = client.post(
        "/users/",
        json=test_data,
    )

    assert response.status_code == 403
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "403"
    assert "message" in json_data and json_data["message"] == f"Telephone number `{test_data['tel_number']}` already registered"


# test get users
def test_get_users(client: TestClient, test_user: dict):
    response = client.get("/users/")

    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "200"


# test get a single user
def test_get_a_single_user(client: TestClient, test_user: dict):
    invalid_user_id = settings.TEST_INVALID_USER_ID

    response = client.get(f"/user/{invalid_user_id}")

    assert response.status_code == 404
    json_data = response.json()

    assert "status" in json_data and json_data["status"] == "404"
    assert (
        "message" in json_data
        and json_data["message"] == f"User with id `{invalid_user_id}` not found",
    )


# test update a given user
def test_update_a_given_users(client: TestClient, test_user: dict):
    valid_user_id = settings.TEST_VALID_USER_ID

    test_data = {
        "fullname": "Update Test User",
        "email": "test_user@gmail.com",
        "tel_number": "0790749459",
        "picture": "https://images.pexels.com/photos/19561453/pexels-photo-19561453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    }

    token = test_login(client, test_user)

    response = client.put(
        f"/users/{valid_user_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=test_data,
    )

    assert response.status_code == 404
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "404"
    assert (
        "message" in json_data
        and json_data["message"] == f"User with id `{valid_user_id}` was not found"
    )


# test deletion of a given user
def test_deletion_of_a_given_user(client: TestClient, test_user: dict):
    invalid_user_id = settings.TEST_VALID_USER_ID

    token = test_login(client, test_user)

    response = client.delete(
        f"/users/{invalid_user_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "404"
    assert (
        "message" in json_data
        and json_data["message"] == f"User with id `{invalid_user_id}` was not found"
    )
