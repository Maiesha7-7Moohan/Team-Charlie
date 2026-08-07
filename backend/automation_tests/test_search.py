from helpers import get


def test_search_valid():
    response = get("/search?q=BBC")
    assert response.status_code == 200


def test_search_returns_list():
    response = get("/search?q=BBC")
    assert isinstance(response.json(), list)


def test_search_missing_query():
    response = get("/search")
    assert response.status_code == 400


def test_search_invalid_query():
    response = get("/search?q=thisdoesnotexist")
    assert response.status_code == 200