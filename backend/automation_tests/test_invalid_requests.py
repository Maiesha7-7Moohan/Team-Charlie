import requests
from config import BASE_URL


def test_invalid_route():
    response = requests.get(f"{BASE_URL}/invalid")
    assert response.status_code == 404


def test_invalid_item():
    response = requests.get(f"{BASE_URL}/items/999999")
    assert response.status_code == 404