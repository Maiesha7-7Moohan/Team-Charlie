from helpers import get


def test_scrape_endpoint_exists():
    response = get("/scrape")
    assert response.status_code == 200


def test_scrape_returns_json():
    response = get("/scrape")
    assert response.headers["Content-Type"].startswith("application/json")


def test_scrape_has_targets():
    response = get("/scrape")
    data = response.json()

    assert "available_targets" in data