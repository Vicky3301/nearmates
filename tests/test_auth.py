def test_login_success(client):
    # Register a user first
    registration_payload = {
        "username": "authtest",
        "email": "authtest@example.com",
        "password": "StrongPassword123",
        "home_region": "Maharashtra",
        "current_city": "Chennai",
    }

    register_response = client.post(
        "/users",
        json=registration_payload,
    )

    assert register_response.status_code == 201

    # Login using form data, not JSON
    login_response = client.post(
        "/auth/login",
        data={
            "username": "authtest@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    registration_payload = {
        "username": "wrongpasstest",
        "email": "wrongpass@example.com",
        "password": "StrongPassword123",
    }

    client.post("/users", json=registration_payload)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "WrongPassword123",
        },
    )

    assert login_response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401