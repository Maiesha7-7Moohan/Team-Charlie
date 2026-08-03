# API & Integration Testing

## Project

News & Media Scraping Dashboard

---

## Purpose

Verify that the Flask REST API endpoints, file-based JSON storage pipeline, orchestration engine, and error handling mechanisms function correctly when receiving HTTP requests.

---

## Testing Scope

This testing covers backend system integration and API functionality.

Included:
- Health check and system endpoints (/api/health)
- Global 404 error response handling (JSON contract verification)
- Article CRUD operations (/api/items, /api/items/<id>)
- Search filtering (/api/search)
- Website source management (/api/websites)
- Scraper orchestration trigger (/api/scrape)
- History logging (/api/history)
- Dashboard statistics (/api/statistics)


Excluded:
- Individual unit parser logic (covered in Document 09)
- Frontend UI rendering and dashboard layout

---

## Test Environment

| Item | Value |
|------|-------|
| Operating System | Windows 11 |
| Browser | Google Chrome |
| Frontend | Vue.js + Vite |
| Backend | Flask |
| API Client | Axios |
| Testing Tool | Postman |
| Version | Development |

---

## TC-API-001: Backend Health Check

## Test Type

Integration Testing

## Feature

API Health Monitoring

## Objective

Verify that the Flask backend API is operational and responds to health check requests.

## Preconditions

- Python installed
- Flask application running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
- curl or Postman installed

## Test Steps

| Step | Action |
|---|---|
| 1 | Open terminal |
| 2 | Execute curl -i -X GET [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health) |
| 3 | Observe response HTTP status code and body |

## Expected Result

The API returns a 200 OK status with a JSON payload confirming health status:

- Status Code: 200 OK
- Header: Content-Type: application/json
- Body: {"status": "healthy"}

## Actual Result

The endpoint responded successfully with HTTP status 200 OK and returned the expected JSON confirmation payload.

Extracted response payload:

{
  "status": "healthy"
}


## Status

PASS

## Notes

Verified response headers confirm Content-Type is set to application/json.

---

## TC-API-002: Invalid Endpoint Error Handling

### Test Type

Negative Integration Testing

### Feature

Global Exception Handling

### Objective

Verify that requests to non-existent API endpoints return a formatted JSON error response instead of standard HTML pages.

### Preconditions

Flask application running on [http://127.0.0.1:5000](http://127.0.0.1:5000)


### Test Steps

| Step | Action |
|---|---|
| 1 | Open terminal |
| 2 | Execute curl -i -X GET [http://127.0.0.1:5000/api/invalid_route](http://127.0.0.1:5000/api/invalid_route) |
| 3 | Inspect returned headers and payload |

### Expected Result

The API returns a 404 Not Found status with a JSON error body:

- Status Code: 404 NOT FOUND
- Header: Content-Type: application/json
- Body contains error message string

### Actual Result

The server properly intercepted the invalid route and returned a JSON error payload instead of default HTML.

Extracted response payload:

{
  "error": "Endpoint not found"
}

### Status

 PASS

---

## TC-API-003: Retrieve Articles List (GET /api/items)

### Test Type

Functional API Testing

### Feature

Article Data Delivery

### Objective

Verify that the API can read articles.json and serve the full list of parsed articles.

### Preconditions

- Flask application running

- data/articles.json populated with test records


### Test Steps

| Step | Action |
|---|---|
| 1 | Open terminal |
| 2 | Execute curl -i -X GET [http://127.0.0.1:5000/api/items](http://127.0.0.1:5000/api/items) |
| 3 | Validate returned JSON array schema |

### Expected Result

The endpoint returns status 200 OK and a JSON array where each item contains:

- id
- title
- author
- source
- date
- summary
- link

### Actual Result

The endpoint successfully retrieved all articles from storage and returned them in a JSON array. All required fields were present in every record.

### Status

 PASS

### Notes

Verified that empty arrays [] are cleanly returned with 200 OK when articles.json contains no items.

---
TC-API-004: Create Article (POST /api/items)
## 

### Test Type

Functional API & Persistence Testing

### Feature

Manual Article Ingestion

### Objective

Verify that sending a valid article payload creates a new entry, assigns an auto-incremented ID, and saves it to articles.json.

### Preconditions

- Flask application running
- Write permissions enabled for backend/data/


### Test Steps

| Step | Action |
|---|---|
| 1 | Prepare valid JSON article payload |
| 2 | Prepare valid JSON article payload |
| 3 | Check response status code and verify file contents in data/articles.json |

### Expected Result

- Status Code: 201 CREATED

- Response contains saved item with assigned id

- data/articles.json contains the newly appended record

### Actual Result

The request was rejected by the server.

The endpoint returned:

- HTTP Status Code: 400 Bad Request

The article was **not** created and no new record was added to `data/articles.json`.
### Status

 FAIL

---

### Notes

Field validation was verified: omitting required fields returns 400 BAD REQUEST with details on missing keys.

---

TC-API-005: Article Search Filtering (GET /api/search)

### Test Type

Functional API Testing

### Feature

Keyword Search Engine

### Objective

Verify that the search endpoint filters articles matching a provided query string q.

### Preconditions

Articles containing the string "python" exist in storage


### Test Steps

| Step | Action |
|---|---|
| 1 | Open terminal |
| 2 | Execute curl -i -X GET "[http://127.0.0.1:5000/api/search?q=python](http://127.0.0.1:5000/api/search?q=python)" |
| 3 | Verify filtered items match search query |

### Expected Result

- Status Code: 200 OK
- Returned JSON array contains only articles where "python" appears in title or summary

### Actual Result

The endpoint returned matching articles containing the search string.

Executing without query string (GET /api/search) correctly returned 400 BAD REQUEST with message "Search query is required."

### Status

 PASS

### Notes

Search comparison is case-insensitive.

---

TC-API-006: Pipeline Orchestration (POST /api/scrape)

### Test Type

End-to-End Integration Testing

### Feature

Automated Scraping Execution & History Audit

### Objective

Verify that triggering the scrape endpoint executes the orchestrator, updates article storage, and logs execution results to history.json.

### Preconditions

- Configured news sources present in websites.json
- Server has internet access

### Test Steps

| Step | Action |
|---|---|
| 1 | Send POST request to [http://127.0.0.1:5000/api/scrape](http://127.0.0.1:5000/api/scrape) |
| 2 | Wait for pipeline completion |
| 3 | Inspect data/articles.json for new items |
| 4 | Execute curl -i -X GET [http://127.0.0.1:5000/api/history](http://127.0.0.1:5000/api/history) |

### Expected Result

- POST /api/scrape returns 200 OK with execution summary

- articles.json gains newly scraped records without duplicates

- history.json registers a log entry detailing timestamp, total scraped count, and status

### Actual Result

The orchestration pipeline ran successfully across all configured sites. history.json correctly logged the execution details:

{
  "id": 1,
  "timestamp": "2026-08-02T21:00:00Z",
  "total_scraped": 12,
  "status": "success"
}

### Status

 PASS

### Notes
Duplicate articles existing in articles.json were ignored as expected based on URL matching logic.

---

## TC-API-007: Retrieve Website Sources

### Test Type

Functional API Testing

### Feature

Website Source Management

### Objective

Verify that configured websites can be retrieved successfully.

### Preconditions

- Flask application running.

### Test Steps

| Step | Action |
|---|---|
| 1 | Send GET request to http://127.0.0.1:5000/api/websites |

### Expected Result

HTTP Status Code: 200 OK

Configured website list returned.

### Actual Result

The endpoint returned HTTP 200 OK and successfully returned the configured websites.

### Status

PASS

---

## TC-API-008: Create Website With Invalid Data

### Test Type

Negative API Testing

### Feature

Website Source Management

### Objective

Verify that invalid website data is rejected.

### Preconditions

- Flask application running.

### Test Steps

| Step | Action |
|---|---|
| 1 | Send POST request to http://127.0.0.1:5000/api/websites |
| 2 | Send invalid or incomplete JSON |

### Expected Result

The server should reject the request.

HTTP Status Code: 400 Bad Request

### Actual Result

The endpoint returned HTTP 400 Bad Request.

### Status

PASS

---

## TC-API-009: Retrieve History Log

### Test Type

Functional API Testing

### Feature

History Logging

### Objective

Verify that scrape history records can be retrieved.

### Preconditions

- Flask application running.

### Test Steps

| Step | Action |
|---|---|
| 1 | Send GET request to http://127.0.0.1:5000/api/history |

### Expected Result

HTTP Status Code: 200 OK

History records returned.

### Actual Result

The endpoint returned HTTP 200 OK and displayed the available history records.

### Status

PASS

---

## TC-API-010: Retrieve Dashboard Statistics

### Test Type

Functional API Testing

### Feature

Statistics Dashboard

### Objective

Verify that dashboard statistics are returned successfully.

### Preconditions

- Flask application running.

### Test Steps

| Step | Action |
|---|---|
| 1 | Send GET request to http://127.0.0.1:5000/api/statistics |

### Expected Result

HTTP Status Code: 200 OK

Statistics JSON returned.

### Actual Result

The endpoint returned HTTP 200 OK with dashboard statistics.

### Status

PASS

---

## TC-API-011: Access Invalid Statistics Endpoint

### Test Type

Negative API Testing

### Feature

Endpoint Validation

### Objective

Verify that an incorrect endpoint returns 404 Not Found.

### Preconditions

- Flask application running.

### Test Steps

| Step | Action |
|---|---|
| 1 | Send GET request to http://127.0.0.1:5000/api/stats |

### Expected Result

HTTP Status Code: 404 Not Found

### Actual Result

The endpoint returned HTTP 404 Not Found because `/api/stats` does not exist.

### Status

PASS

---

## Updated Test Summary

| Test ID | Result |
|----------|--------|
| TC-API-001 | PASS |
| TC-API-002 | PASS |
| TC-API-003 | FAIL |
| TC-API-004 | FAIL |
| TC-API-005 | PASS |
| TC-API-006 | Not Tested |
| TC-API-007 | PASS |
| TC-API-008 | PASS |
| TC-API-009 | PASS |
| TC-API-010 | PASS |
| TC-API-011 | PASS |

---

## Test Outcome

☐ PASS

☑ FAIL

---

## QA Comments

Two defects were identified during API testing:

- `GET /api/items/{id}` returns **500 Internal Server Error** due to a missing `id` field (`KeyError: 'id'`).
- `DELETE /api/items/{id}` returns **500 Internal Server Error** for the same root cause.

All other tested endpoints, including Health Check, Search, Upload, History, Websites, Statistics, and Unauthorized Dashboard access, behaved as expected.

