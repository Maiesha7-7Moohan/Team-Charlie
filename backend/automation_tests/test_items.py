from helpers import get


def test_get_items():
    response = get("/items")
    assert response.status_code == 200


def test_items_json():
    response = get("/items")
    assert response.headers["Content-Type"].startswith("application/json")


def test_items_structure():
    response = get("/items")
    data = response.json()

    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "items" in data


def test_items_is_list():
    response = get("/items")
    data = response.json()

    assert isinstance(data["items"], list)


def test_first_item_has_title():
    response = get("/items")
    data = response.json()

    if len(data["items"]) > 0:
        assert "title" in data["items"][0]