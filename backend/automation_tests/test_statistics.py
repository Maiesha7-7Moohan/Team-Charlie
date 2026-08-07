from helpers import get


def test_statistics_status():
    response = get("/statistics")
    assert response.status_code == 200


def test_statistics_json():
    response = get("/statistics")
    assert response.headers["Content-Type"].startswith("application/json")


def test_statistics_fields():
    response = get("/statistics")
    data = response.json()

    assert "total_articles" in data
    assert "total_sources" in data
    assert "total_websites" in data
    assert "success_rate" in data