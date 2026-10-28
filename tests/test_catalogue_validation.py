def test_languages_endpoint_returns_list(client):
    response = client.get("/languages")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_interests_endpoint_returns_list(client):
    response = client.get("/interests")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_language_catalogue_has_valid_items(client):
    response = client.get("/languages")

    assert response.status_code == 200

    for item in response.json():
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert item["name"].strip() != ""


def test_interest_catalogue_has_valid_items(client):
    response = client.get("/interests")

    assert response.status_code == 200

    for item in response.json():
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert item["name"].strip() != ""


def test_language_ids_are_unique(client):
    response = client.get("/languages")

    assert response.status_code == 200

    ids = [item["id"] for item in response.json()]

    assert len(ids) == len(set(ids))


def test_interest_ids_are_unique(client):
    response = client.get("/interests")

    assert response.status_code == 200

    ids = [item["id"] for item in response.json()]

    assert len(ids) == len(set(ids))


def test_language_names_are_unique_case_insensitively(client):
    response = client.get("/languages")

    assert response.status_code == 200

    names = [
        item["name"].casefold()
        for item in response.json()
    ]

    assert len(names) == len(set(names))


def test_interest_names_are_unique_case_insensitively(client):
    response = client.get("/interests")

    assert response.status_code == 200

    names = [
        item["name"].casefold()
        for item in response.json()
    ]

    assert len(names) == len(set(names))