# Team Charlie API Documentation

## Overview
The Team Charlie backend is built using Flask and provides a REST API for managing news articles, website sources, scraping, statistics, and history.

The API reads and writes JSON files stored in the backend/data directory.

---

The API supports:

- Health checks
- Article management (CRUD)
- Article search
- Website management
- Scraper history
- Statistics

---

Technologies:
- Python 3.x
- Flask
- Flask-CORS
- BeautifulSoup4
- Requests
- lxml (XML parser)

---

# Installation
Clone the repository:

```
bash
git clone <repository-url>
cd Team-Charlie
```

Create a virtual environment:

```
bash
python -m venv .venv
```
Activate it.

**Windows**

```
bash
.venv\Scripts\activate
```

Install dependencies:
```
bash
pip install -r requirements.txt
```

Run the application:
```
bash
python backend/app.py
```
---

# Base URL
http://127.0.0.1:5000/api

---

# Health Check

## GET /health

Checks whether the API is running.

### Parameters

None.

### Example Response

```json
{
    "status": "healthy",
    "message": "Team Charlie API is running!"
}
```

### Status Codes

- 200 OK

---

# Get All Articles

## GET /items

Returns a paginated list of articles.

### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| page | Integer | Page number (default: 1) |
| limit | Integer | Number of articles per page (default: 20) |

### Example Response

```json
{
    "page": 1,
    "limit": 20,
    "total": 248,
    "items": [
        {
            "title": "Police officer was violent rapist...",
            "description": "The BBC can reveal...",
            "published": "2026-07-23 05:12:30",
            "author": "",
            "category": "News",
            "source": "BBC",
            "image_url": "",
            "article": "",
            "link": "https://www.bbc.co.uk/news/..."
        }
    ]
}
```

### Status Codes

- 200 OK

---

# Get Article by ID

## GET /items/{id}

Returns a single article.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| id | Integer | Article ID |

### Example Response

```json
{
    "id": 10,
    "title": "Example Article",
    "description": "Example description.",
    "published": "2026-07-23 10:15:00",
    "author": "",
    "category": "News",
    "source": "BBC",
    "image_url": "",
    "article": "",
    "link": "https://..."
}
```

If the article cannot be found:

```json
{
    "error": "Article not found."
}
```

### Status Codes

- 200 OK
- 404 Not Found

---

# Search Articles

## GET /search?q=keyword

Searches for articles matching the supplied keyword.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| q | String | Search keyword |

### Status Codes

- 200 OK
- 400 Bad Request

---

# Create Article

## POST /items

Creates a new article.

### Request Body

```json
{
    "title": "Example Article",
    "description": "Example description",
    "author": "John Smith",
    "published": "2026-08-04 10:00:00",
    "source": "BBC",
    "category": "Technology",
    "image_url": "",
    "article": "",
    "link": "https://example.com"
}
```

### Example Response

```json
{
    "id": 249,
    "title": "Example Article",
    "description": "Example description",
    "author": "John Smith",
    "published": "2026-08-04 10:00:00",
    "source": "BBC",
    "category": "Technology",
    "image_url": "",
    "article": "",
    "link": "https://example.com"
}
```

### Status Codes

- 201 Created
- 400 Bad Request

---

# Update Article

## PUT /items/{id}

Updates an existing article.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| id | Integer | Article ID |

### Request Body

```json
{
    "title": "Updated Article",
    "description": "Updated description",
    "author": "John Smith",
    "published": "2026-08-04 10:00:00",
    "source": "BBC",
    "category": "Technology",
    "image_url": "",
    "article": "",
    "link": "https://example.com"
}
```

### Example Response

```json
{
    "id": 249,
    "title": "Updated Article",
    "description": "Updated description",
    "author": "John Smith",
    "published": "2026-08-04 10:00:00",
    "source": "BBC",
    "category": "Technology",
    "image_url": "",
    "article": "",
    "link": "https://example.com"
}
```

### Status Codes

- 200 OK
- 400 Bad Request
- 404 Not Found

---

# Delete Article

## DELETE /items/{id}

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

### Status Codes

- 200 OK
- 404 Not Found

---

# Get Websites

## GET /websites

Returns all configured websites used for scraping.

### Example Response

```json
[
    {
        "name": "BBC",
        "url": "https://www.bbc.com/news"
    },
    {
        "name": "CNN",
        "url": "https://www.cnn.com"
    }
]
```

### Status Codes

- 200 OK

---

# Add Website

## POST /websites

Adds a new website.

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

### Status Codes

- 201 Created
- 400 Bad Request

---

# Scraper History

## GET /history

Returns previous scraper runs.

### Example Response

```json
[
    {
        "timestamp": "2026-08-04T14:30:00",
        "website": "BBC",
        "articles_found": 25
    }
]
```

### Status Codes

- 200 OK

---

# Statistics

## GET /statistics

Returns basic statistics about the stored articles.

### Example Response

```json
{
    "total_articles": 248,
    "total_sources": 4
}
```

### Status Codes

- 200 OK

---

# Scraper

## POST /scrape

Runs one or more configured news scrapers.

### Request Body

```json
{
    "target": "bbc"
}
```

Supported targets include:

- BBC
- CNN
- TechCrunch
- CoinDesk

### Example Response

```json
{
    "message": "Scraper endpoint is ready. Waiting for website details."
}
```

### Status Codes

- 200 OK

---

## Typical HTTP responses:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

## Notes
- JSON files are used as the application's data store.
- Articles support CRUD (Create, Read, Update, Delete) operations.
- Pagination is available on the /api/items endpoint.
- The scraper modules collect articles from multiple news sources and save them as JSON.

## Known Limitation

Some older articles contained in `articles_cleaned.json` may not include an `id` field. CRUD operations that rely on article IDs require articles to contain unique identifiers.

## My Contribution (Karah Fisher)

I was responsible for the Flask backend API. My responsibilities included:

- Creating and registering Flask Blueprints
- Implementing REST API endpoints
- Developing CRUD operations for articles
- Integrating scraper routes
- Implementing HTTP status codes and error handling
- Testing API endpoints
- Investigating and fixing backend bugs
- Updating the API documentation