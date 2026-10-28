def register_and_login(client, username, email, password):
    registration = client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": password,
            "home_region": "Maharashtra",
            "current_city": "Chennai",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login.status_code == 200

    return login.json()["access_token"]


def test_login_success(client):
    token = register_and_login(
        client,
        "loginuser",
        "loginuser@example.com",
        "StrongPassword123",
    )

    assert isinstance(token, str)
    assert len(token) > 20


def test_login_wrong_password(client):
    client.post(
        "/users",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "StrongPassword123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "IncorrectPassword123",
        },
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nobody@example.com",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401


def test_authenticated_user_can_access_profile(client):
    token = register_and_login(
        client,
        "profileuser",
        "profileuser@example.com",
        "StrongPassword123",
    )

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "profileuser@example.com"