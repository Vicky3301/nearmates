def test_get_languages(client):
    response = client.get("/languages")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_interests(client):
    response = client.get("/interests")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_language_items_have_ids_and_names(client):
    response = client.get("/languages")

    assert response.status_code == 200

    for item in response.json():
        assert "id" in item
        assert "name" in item


def test_interest_items_have_ids_and_names(client):
    response = client.get("/interests")

    assert response.status_code == 200

    for item in response.json():
        assert "id" in item
        assert "name" in item