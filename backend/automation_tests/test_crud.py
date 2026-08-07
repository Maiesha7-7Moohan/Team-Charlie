from helpers import post, put, delete

article = {
    "title": "Pytest Article",
    "description": "Testing",
    "author": "QA",
    "published": "2026-08-06 12:00:00",
    "source": "BBC",
    "category": "Testing",
    "image_url": "",
    "article": "",
    "link": "https://pytest.com"
}


def test_create_article():

    response = post("/items", article)

    assert response.status_code == 201


def test_update_missing_article():

    response = put("/items/999999", article)

    assert response.status_code == 404


def test_delete_missing_article():

    response = delete("/items/999999")

    assert response.status_code == 404