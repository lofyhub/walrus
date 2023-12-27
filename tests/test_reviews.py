from fastapi.testclient import TestClient
import io
from .test_auth import client, test_login, test_user
from .test_review_business import read_image
from src.auth.auth import get_user_from_token


def test_post_review_business(client: TestClient, test_user: dict):
    image_data = [
        read_image("safety-dance.jpg"),
    ]

    image_files = [
        ("images", ("image1.jpeg", io.BytesIO(image_data[0]), "image/jpeg")),
    ]

    token = test_login(client, test_user)
    user_id = get_user_from_token(token)["user_id"]

    test_data = {
        "text": "This is a sample review text.",
        "rating": "5",
        "business_id": "04075ed7f6df4720a0db478fca6de3e8",  # TODO: USE DYNAMIC BUSINESS_ID
        "user_id": user_id,
    }
    response = client.post(
        "/reviews/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        data=test_data,
        files=image_files,
    )

    assert response.status_code == 201
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "201"
    assert (
        "message" in json_data and json_data["message"] == "Review successfully saved"
    )


# test get review
def test_get_review_business(client: TestClient, test_user: dict):
    response = client.get("/reviews/")

    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "200"


# test get a single review
def test_get_reviews_of_a_specific_business(client: TestClient, test_user: dict):
    invalid_id = "00d75e56-a5b7-4655-91b0-210cb4bd8e54"

    response = client.get(f"/review/{invalid_id}")

    assert response.status_code == 200
    json_data = response.json()

    assert "status" in json_data and json_data["status"] == "200"
    assert (
        "message" in json_data
        and json_data["message"]
        == f"Reviews for Business with id: `{invalid_id}` not found"
    )


# test update a given review
def test_update_reviews_of_a_specific_business(client: TestClient, test_user: dict):
    valid_review_id = "5e3706b0-5f6f-4ac7-92ec-a6ad0a0ba5db"

    test_data = {
        "text": "This is a sample review text.",
        "rating": "5",
    }

    token = test_login(client, test_user)

    response = client.put(
        f"/reviews/{valid_review_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=test_data,
    )

    assert response.status_code == 403
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "403"
    assert (
        "message" in json_data
        and json_data["message"] == "You can only update your resource"
    )


# test deletion of a given review
def test_deletion_of_a_given_review(client: TestClient, test_user: dict):
    invalid_review_id = "3611b048-7d4d-46f1-bf31-698e673056e1"

    token = test_login(client, test_user)

    response = client.delete(
        f"/reviews/{invalid_review_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "404"
    assert (
        "message" in json_data
        and json_data["message"]
        == f"Review with id `{invalid_review_id}` was not found"
    )
