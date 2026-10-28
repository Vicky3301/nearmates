def get_discovery_headers(client, username, email):
    registration = client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": "StrongPassword123",
            "home_region": "Maharashtra",
            "current_city": "Chennai",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "StrongPassword123",
        },
    )

    assert login.status_code == 200

    return {
        "Authorization": (
            f"Bearer {login.json()['access_token']}"
        )
    }


def test_discovery_rejects_page_zero(client):
    headers = get_discovery_headers(
        client,
        "pagezero",
        "pagezero@example.com",
    )

    response = client.get(
        "/discover?page=0",
        headers=headers,
    )

    assert response.status_code == 422


def test_discovery_rejects_negative_page(client):
    headers = get_discovery_headers(
        client,
        "negativepage",
        "negativepage@example.com",
    )

    response = client.get(
        "/discover?page=-1",
        headers=headers,
    )

    assert response.status_code == 422


def test_discovery_rejects_page_size_zero(client):
    headers = get_discovery_headers(
        client,
        "pagesizezero",
        "pagesizezero@example.com",
    )

    response = client.get(
        "/discover?page_size=0",
        headers=headers,
    )

    assert response.status_code == 422


def test_discovery_rejects_page_size_over_limit(client):
    headers = get_discovery_headers(
        client,
        "pagesizelarge",
        "pagesizelarge@example.com",
    )

    response = client.get(
        "/discover?page_size=51",
        headers=headers,
    )

    assert response.status_code == 422


def test_discovery_rejects_non_numeric_page(client):
    headers = get_discovery_headers(
        client,
        "pagenonnumeric",
        "pagenonnumeric@example.com",
    )

    response = client.get(
        "/discover?page=abc",
        headers=headers,
    )

    assert response.status_code == 422


def test_discovery_rejects_non_numeric_page_size(client):
    headers = get_discovery_headers(
        client,
        "pagesizenonnumeric",
        "pagesizenonnumeric@example.com",
    )

    response = client.get(
        "/discover?page_size=abc",
        headers=headers,
    )

    assert response.status_code == 422