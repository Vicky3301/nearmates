def test_discovery_requires_authentication(client):
    response = client.get("/discover")

    assert response.status_code == 401


def test_discovery_returns_expected_structure(client):
    registration = client.post(
        "/users",
        json={
            "username": "discoveryuser",
            "email": "discoveryuser@example.com",
            "password": "StrongPassword123",
            "home_region": "Maharashtra",
            "current_city": "Chennai",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": "discoveryuser@example.com",
            "password": "StrongPassword123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/discover",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10
    assert "total" in data
    assert "results" in data
    assert isinstance(data["results"], list)


def test_discovery_rejects_invalid_page(client):
    registration = client.post(
        "/users",
        json={
            "username": "pageuser",
            "email": "pageuser@example.com",
            "password": "StrongPassword123",
            "current_city": "Chennai",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": "pageuser@example.com",
            "password": "StrongPassword123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/discover?page=0",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_discovery_rejects_oversized_page_size(client):
    registration = client.post(
        "/users",
        json={
            "username": "pagesizeuser",
            "email": "pagesizeuser@example.com",
            "password": "StrongPassword123",
            "current_city": "Chennai",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": "pagesizeuser@example.com",
            "password": "StrongPassword123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/discover?page_size=100",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422