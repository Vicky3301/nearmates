def create_discovery_user(client, username, email, city="Chennai"):
    registration = client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": "StrongPassword123",
            "home_region": "Maharashtra",
            "current_city": city,
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

    return login.json()["access_token"]


def test_discovery_does_not_return_password_fields(client):
    token = create_discovery_user(
        client,
        "responseowner",
        "responseowner@example.com",
    )

    create_discovery_user(
        client,
        "responsecandidate",
        "responsecandidate@example.com",
    )

    response = client.get(
        "/discover",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    for user in response.json()["results"]:
        assert "password" not in user
        assert "password_hash" not in user
        assert "hashed_password" not in user


def test_discovery_results_contain_required_fields(client):
    token = create_discovery_user(
        client,
        "fieldowner",
        "fieldowner@example.com",
    )

    create_discovery_user(
        client,
        "fieldcandidate",
        "fieldcandidate@example.com",
    )

    response = client.get(
        "/discover",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    required_fields = {
        "user_id",
        "username",
        "home_region",
        "current_city",
        "bio",
        "shared_languages",
        "shared_interests",
        "match_score",
    }

    for user in response.json()["results"]:
        assert required_fields.issubset(user.keys())


def test_discovery_match_score_is_between_zero_and_one_hundred(client):
    token = create_discovery_user(
        client,
        "scoreowner",
        "scoreowner@example.com",
    )

    create_discovery_user(
        client,
        "scorecandidate",
        "scorecandidate@example.com",
    )

    response = client.get(
        "/discover",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    for user in response.json()["results"]:
        assert 0 <= user["match_score"] <= 100


def test_discovery_results_are_deterministically_ordered(client):
    token = create_discovery_user(
        client,
        "orderingowner",
        "orderingowner@example.com",
    )

    create_discovery_user(
        client,
        "zulu_candidate",
        "zulu_candidate@example.com",
    )

    create_discovery_user(
        client,
        "alpha_candidate",
        "alpha_candidate@example.com",
    )

    response = client.get(
        "/discover",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    results = response.json()["results"]

    sort_keys = [
        (
            -user["match_score"],
            user["username"].casefold(),
            user["user_id"],
        )
        for user in results
    ]

    assert sort_keys == sorted(sort_keys)