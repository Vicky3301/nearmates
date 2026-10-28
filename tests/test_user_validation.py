import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": "ab",
            "email": "shortname@example.com",
            "password": "StrongPassword123",
        },
        {
            "username": "validuser",
            "email": "not-an-email",
            "password": "StrongPassword123",
        },
        {
            "username": "validuser",
            "email": "shortpassword@example.com",
            "password": "123",
        },
        {
            "username": "validuser",
            "email": "missingpassword@example.com",
        },
        {
            "email": "missingusername@example.com",
            "password": "StrongPassword123",
        },
    ],
)
def test_invalid_registration_payloads_rejected(client, payload):
    response = client.post("/users", json=payload)

    assert response.status_code == 422


def test_username_max_length_enforced(client):
    response = client.post(
        "/users",
        json={
            "username": "u" * 51,
            "email": "longusername@example.com",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 422


def test_bio_max_length_enforced(client):
    response = client.post(
        "/users",
        json={
            "username": "biotest",
            "email": "biotest@example.com",
            "password": "StrongPassword123",
            "bio": "a" * 501,
        },
    )

    assert response.status_code == 422


def test_password_hash_is_not_exposed(client):
    response = client.post(
        "/users",
        json={
            "username": "securityuser",
            "email": "securityuser@example.com",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "password" not in data
    assert "password_hash" not in data
    assert "hashed_password" not in data