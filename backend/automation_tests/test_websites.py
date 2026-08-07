from helpers import get


def test_websites_status():
    response = get("/websites")
    assert response.status_code == 200


def test_websites_json():
    response = get("/websites")
    assert response.headers["Content-Type"].startswith("application/json")


def test_websites_returns_list():
    response = get("/websites")
    assert isinstance(response.json(), list)