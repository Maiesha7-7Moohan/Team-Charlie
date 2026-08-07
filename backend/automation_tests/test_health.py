from helpers import get


def test_health_status():
    response = get("/health")
    assert response.status_code == 200


def test_health_json():
    response = get("/health")
    assert response.headers["Content-Type"].startswith("application/json")


def test_health_keys():
    response = get("/health")
    data = response.json()

    assert "status" in data
    assert "message" in data


def test_health_response_time():
    response = get("/health")
    assert response.elapsed.total_seconds() < 2