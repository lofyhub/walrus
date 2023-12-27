from fastapi.testclient import TestClient
import os
import io
from .test_auth import client, test_login, test_user


def get_image_path(filename):
    return os.path.join(os.path.dirname(__file__), "test_images", filename)


def read_image(filename):
    with open(get_image_path(filename), "rb") as f:
        return f.read()


def test_review_business(client: TestClient, test_user: dict):
    image_data = [
        read_image("safety-dance.jpg"),
        read_image("rust_mascot_with_hat.jpeg"),
    ]

    image_files = [
        ("images", ("image1.jpeg", io.BytesIO(image_data[0]), "image/jpeg")),
        ("images", ("image2.jpeg", io.BytesIO(image_data[1]), "image/jpeg")),
    ]

    test_data = {
        "name": "Test Business",
        "county": "Test County",
        "town": "Test Town",
        "category": "Test Category",
        "amenities": ["Amenity1", "Amenity2"],
        "star": "5",
        "review": "Test Review",
    }

    token = test_login(client, test_user)

    response = client.post(
        "/reviewed_businesses/",
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
        "message" in json_data
        and json_data["message"] == "Business Review successfully saved"
    )
