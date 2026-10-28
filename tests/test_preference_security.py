def register_and_get_headers(client, username, email):
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


def test_preferences_reject_missing_authentication(client):
    language_response = client.put(
        "/users/me/languages",
        json={"ids": [1]},
    )

    interest_response = client.put(
        "/users/me/interests",
        json={"ids": [1]},
    )

    assert language_response.status_code == 401
    assert interest_response.status_code == 401


def test_duplicate_language_ids_rejected(client):
    headers = register_and_get_headers(
        client,
        "duplicatelang",
        "duplicatelang@example.com",
    )

    catalogue = client.get("/languages")
    assert catalogue.status_code == 200

    languages = catalogue.json()

    if not languages:
        return

    language_id = languages[0]["id"]

    response = client.put(
        "/users/me/languages",
        json={"ids": [language_id, language_id]},
        headers=headers,
    )

    assert response.status_code in (400, 422)


def test_duplicate_interest_ids_rejected(client):
    headers = register_and_get_headers(
        client,
        "duplicateinterest",
        "duplicateinterest@example.com",
    )

    catalogue = client.get("/interests")
    assert catalogue.status_code == 200

    interests = catalogue.json()

    if not interests:
        return

    interest_id = interests[0]["id"]

    response = client.put(
        "/users/me/interests",
        json={"ids": [interest_id, interest_id]},
        headers=headers,
    )

    assert response.status_code in (400, 422)


def test_empty_language_selection_validation(client):
    headers = register_and_get_headers(
        client,
        "emptylanguages",
        "emptylanguages@example.com",
    )

    response = client.put(
        "/users/me/languages",
        json={"ids": []},
        headers=headers,
    )

    # Your current schema requires at least one ID.
    assert response.status_code == 422


def test_empty_interest_selection_validation(client):
    headers = register_and_get_headers(
        client,
        "emptyinterests",
        "emptyinterests@example.com",
    )

    response = client.put(
        "/users/me/interests",
        json={"ids": []},
        headers=headers,
    )

    # Your current schema requires at least one ID.
    assert response.status_code == 422


def test_invalid_language_id_does_not_corrupt_existing_preferences(client):
    headers = register_and_get_headers(
        client,
        "languageintegrity",
        "languageintegrity@example.com",
    )

    catalogue = client.get("/languages")
    assert catalogue.status_code == 200

    languages = catalogue.json()

    if not languages:
        return

    valid_id = languages[0]["id"]

    save_response = client.put(
        "/users/me/languages",
        json={"ids": [valid_id]},
        headers=headers,
    )

    assert save_response.status_code == 200

    invalid_response = client.put(
        "/users/me/languages",
        json={"ids": [999999999]},
        headers=headers,
    )

    assert invalid_response.status_code in (400, 422)

    current_response = client.get(
        "/users/me/languages",
        headers=headers,
    )

    assert current_response.status_code == 200

    saved_ids = [
        item["id"] for item in current_response.json()
    ]

    assert valid_id in saved_ids