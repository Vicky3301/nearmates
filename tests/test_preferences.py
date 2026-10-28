def create_authenticated_user(client, username, email):
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

    token = login.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_get_my_languages_requires_authentication(client):
    response = client.get("/users/me/languages")

    assert response.status_code == 401


def test_get_my_interests_requires_authentication(client):
    response = client.get("/users/me/interests")

    assert response.status_code == 401


def test_save_language_preferences(client):
    headers = create_authenticated_user(
        client,
        "languageuser",
        "languageuser@example.com",
    )

    catalogue_response = client.get("/languages")
    assert catalogue_response.status_code == 200

    languages = catalogue_response.json()

    if not languages:
        return

    language_id = languages[0]["id"]

    response = client.put(
        "/users/me/languages",
        json={"ids": [language_id]},
        headers=headers,
    )

    assert response.status_code == 200

    saved = client.get(
        "/users/me/languages",
        headers=headers,
    )

    assert saved.status_code == 200
    assert language_id in [item["id"] for item in saved.json()]


def test_save_interest_preferences(client):
    headers = create_authenticated_user(
        client,
        "interestuser",
        "interestuser@example.com",
    )

    catalogue_response = client.get("/interests")
    assert catalogue_response.status_code == 200

    interests = catalogue_response.json()

    if not interests:
        return

    interest_id = interests[0]["id"]

    response = client.put(
        "/users/me/interests",
        json={"ids": [interest_id]},
        headers=headers,
    )

    assert response.status_code == 200

    saved = client.get(
        "/users/me/interests",
        headers=headers,
    )

    assert saved.status_code == 200
    assert interest_id in [item["id"] for item in saved.json()]


def test_invalid_language_id_rejected(client):
    headers = create_authenticated_user(
        client,
        "invalidlang",
        "invalidlang@example.com",
    )

    response = client.put(
        "/users/me/languages",
        json={"ids": [999999999]},
        headers=headers,
    )

    assert response.status_code in (400, 422)


def test_invalid_interest_id_rejected(client):
    headers = create_authenticated_user(
        client,
        "invalidinterest",
        "invalidinterest@example.com",
    )

    response = client.put(
        "/users/me/interests",
        json={"ids": [999999999]},
        headers=headers,
    )

    assert response.status_code in (400, 422)