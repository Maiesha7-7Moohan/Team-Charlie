import requests
from config import BASE_URL, TIMEOUT


def get(endpoint):
    return requests.get(
        f"{BASE_URL}{endpoint}",
        timeout=TIMEOUT
    )


def post(endpoint, payload=None):
    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        timeout=TIMEOUT
    )


def put(endpoint, payload=None):
    return requests.put(
        f"{BASE_URL}{endpoint}",
        json=payload,
        timeout=TIMEOUT
    )


def delete(endpoint):
    return requests.delete(
        f"{BASE_URL}{endpoint}",
        timeout=TIMEOUT
    )