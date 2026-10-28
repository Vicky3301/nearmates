def register_user(client, username, email, password="StrongPassword123"):
    return client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": password,
            "home_region": "Maharashtra",
            "current_city": "Chennai",
        },
    )


def login_user(client, email, password="StrongPassword123"):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def test_nonexistent_user_cannot_login(client):
    response = login_user(
        client,
        "nonexistent@example.com",
    )

    assert response.status_code == 401


def test_empty_password_rejected(client):
    register_response = register_user(
        client,
        "emptypassuser",
        "emptypass@example.com",
    )

    assert register_response.status_code == 201

    response = login_user(
        client,
        "emptypass@example.com",
        password="",
    )

    assert response.status_code == 401


def test_invalid_bearer_token_rejected(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer not-a-valid-token",
        },
    )

    assert response.status_code == 401


def test_missing_bearer_token_rejected(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_login_returns_bearer_token(client):
    registration = register_user(
        client,
        "tokenuser",
        "tokenuser@example.com",
    )

    assert registration.status_code == 201

    response = login_user(
        client,
        "tokenuser@example.com",
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20
    assert data["token_type"].lower() == "bearer"


def test_wrong_password_does_not_authenticate(client):
    registration = register_user(
        client,
        "wrongpassworduser",
        "wrongpassworduser@example.com",
    )

    assert registration.status_code == 201

    login_response = login_user(
        client,
        "wrongpassworduser@example.com",
        password="IncorrectPassword123",
    )

    assert login_response.status_code == 401


def test_authenticated_profile_matches_logged_in_user(client):
    registration = register_user(
        client,
        "profilecheck",
        "profilecheck@example.com",
    )

    assert registration.status_code == 201

    login_response = login_user(
        client,
        "profilecheck@example.com",
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    profile_response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "profilecheck@example.com"