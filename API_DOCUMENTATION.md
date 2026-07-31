# Team Charlie API Documentation

## Base URL

```
http://127.0.0.1:5000/api
```

---

# Health Check

### GET /health

Checks that the backend server is running.

### Parameters

None.

### Example Response

```json
{
    "status": "ok"
}
```

Status Code:

- 200 OK

---

# Get All Articles

### GET /items

Returns all stored articles.

### Parameters

None.

### Example Response

```json
[
    {
        "id": 1,
        "title": "Python Basics",
        "author": "Alice",
        "source": "BBC",
        "date": "2025-07-20",
        "summary": "Introduction to Python."
    }
]
```

Status Code:

- 200 OK

---

# Get Article by ID

### GET /items/{id}

Returns a single article.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| id | Integer | Article ID |

### Example Response

```json
{
    "id": 1,
    "title": "Python Basics",
    "author": "Alice",
    "source": "BBC",
    "date": "2025-07-20",
    "summary": "Introduction to Python."
}
```

If the article doesn't exist:

```json
{
    "error": "Article not found."
}
```

Status Codes:

- 200 OK
- 404 Not Found

---

# Search Articles

### GET /search?q=python

Searches article titles.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| q | String | Search keyword |

### Example Response

```json
[
    {
        "id": 2,
        "title": "Learning Python",
        "author": "Bob",
        "source": "News24",
        "date": "2025-07-19",
        "summary": "Python tutorial."
    }
]
```

Possible Errors

```json
{
    "error": "Search query is required."
}
```

Status Codes

- 200 OK
- 400 Bad Request

---

# Create Article

### POST /items

Creates a new article.

### Request Body

```json
{
    "title": "Flask Guide",
    "author": "Karah",
    "source": "BBC",
    "date": "2025-07-27",
    "summary": "Introduction to Flask."
}
```

### Example Response

```json
{
    "id": 5,
    "title": "Flask Guide",
    "author": "Karah",
    "source": "BBC",
    "date": "2025-07-27",
    "summary": "Introduction to Flask."
}
```

Status Codes

- 201 Created
- 400 Bad Request

---

# Update Article

### PUT /items/{id}

Updates an existing article.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| id | Integer | Article ID |

### Request Body

```json
{
    "title": "Updated Title",
    "author": "Karah",
    "source": "BBC",
    "date": "2025-07-27",
    "summary": "Updated summary."
}
```

### Example Response

```json
{
    "id": 5,
    "title": "Updated Title",
    "author": "Karah",
    "source": "BBC",
    "date": "2025-07-27",
    "summary": "Updated summary."
}
```

Status Codes

- 200 OK
- 400 Bad Request
- 404 Not Found

---

# Delete Article

### DELETE /items/{id}

Deletes an article.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| id | Integer | Article ID |

### Example Response

```json
{
    "message": "Article deleted successfully."
}
```

Status Codes

- 200 OK
- 404 Not Found

---

# Get Websites

### GET /websites

Returns all configured scraping websites.

### Parameters

None.

### Example Response

```json
[
    {
        "name": "BBC",
        "url": "https://www.bbc.com/news"
    }
]
```

Status Code

- 200 OK

---

# Add Website

### POST /websites

Adds a website to the scraping list.

### Request Body

```json
{
    "name": "BBC",
    "url": "https://www.bbc.com/news"
}
```

### Example Response

```json
{
    "name": "BBC",
    "url": "https://www.bbc.com/news"
}
```

Status Codes

- 201 Created
- 400 Bad Request

---

# Scraping History

### GET /history

Returns previous scraper runs.

### Parameters

None.

### Example Response

```json
[
    {
        "timestamp": "2025-07-27T10:15:00",
        "website": "BBC",
        "articles_found": 15
    }
]
```

Status Code

- 200 OK

---

# Statistics

### GET /stats

Returns scraper statistics.

### Example Response

```json
{
    "total_articles": 150,
    "total_websites": 4,
    "last_scrape": "2025-07-27T10:15:00"
}
```

Status Code

- 200 OK