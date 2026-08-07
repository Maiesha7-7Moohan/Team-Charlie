import time

from helpers import get


def test_items_speed():
    start = time.time()
    response = get("/items")
    end = time.time()

    assert response.status_code == 200
    assert end - start < 2


def test_statistics_speed():
    start = time.time()
    response = get("/statistics")
    end = time.time()

    assert response.status_code == 200
    assert end - start < 2