from helpers import get


def test_history_status():
    response = get("/history")
    assert response.status_code == 200


def test_history_is_list():
    response = get("/history")
    assert isinstance(response.json(), list)