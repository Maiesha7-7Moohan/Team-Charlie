# Backend Bug Reports

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |

---

# Purpose

The purpose of this document is to record all backend issues discovered during testing.

Each bug report includes:

- What went wrong
- How to reproduce the problem
- What should happen
- What actually happened
- The impact of the issue

This helps developers understand and fix problems quickly.

---

# Bug Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Application cannot be used or major functionality is broken |
| High | Important feature does not work correctly |
| Medium | Feature works but has problems affecting users |
| Low | Small issue with limited impact |

---

# Bug List

| Bug ID | Title | Severity | Status |
|--------|-------|----------|--------|
| BUG-001 | GET /api/items/{id} returns 500 server error | High | Open |
| BUG-002 | DELETE request for missing item returns incorrect response | Medium | Open |
| | | | |

---

# BUG-001

## Title

GET /api/items/{id} returns 500 Internal Server Error

---

## Severity

High

---

## Status

Open

---

## Environment

| Item | Details |
|------|---------|
| Backend | Flask |
| API Endpoint | GET /api/items/{id} |
| Testing Tool | Postman |
| Operating System | Windows 11 |

---

## Description

When requesting a single article using its ID, the API does not return the requested article.

Instead, the server crashes and returns a 500 Internal Server Error.

---

## Steps to Reproduce

1. Start the Flask backend server.
2. Open Postman.
3. Send a GET request:

```
GET http://127.0.0.1:5000/api/items/1
```

4. Check the response.

---

## Expected Result

The API should return:

- Status code 200 OK
- The article information
- Valid JSON response

Example:

```json
{
    "id": 1,
    "title": "Example Article",
    "description": "Article description"
}
```

---

## Actual Result

The API returns:

```
500 Internal Server Error
```

The backend crashes because the requested article data does not contain the expected `id` field.

---

## Error Details

Backend error:

```
KeyError: 'id'
```

Location:

```
routes/items.py
```

---

## Impact

Users cannot open or view individual articles from the dashboard.

The frontend cannot display article details because the backend request fails.

---

## Evidence

Screenshot:

```
testing/backend/screenshots/API-002-item-id-error.png
```

---

## Recommended Fix

Developer should verify that:

- Every article object contains an `id` field.
- The API handles missing fields safely.
- A 404 response is returned when an article does not exist.

---

# BUG-002

## Title

DELETE request for missing article does not return expected response

---

## Severity

Medium

---

## Status

Open

---

## Environment

| Item | Details |
|------|---------|
| Backend | Flask |
| API Endpoint | DELETE /api/items/{id} |
| Testing Tool | Postman |

---

## Description

When attempting to delete an article that does not exist, the API response does not match the expected behaviour.

---

## Steps to Reproduce

1. Open Postman.
2. Send:

```
DELETE http://127.0.0.1:5000/api/items/9999
```

3. View the response.

---

## Expected Result

The API should return:

```
404 Not Found
```

with a clear error message.

Example:

```json
{
    "message": "Article not found"
}
```

---

## Actual Result

The API returns an unexpected response.

---

## Impact

Users may not understand whether the delete action succeeded or failed.

---

## Evidence

Screenshot:

```
testing/backend/screenshots/API-delete-invalid-id.png
```

---

## Recommended Fix

The backend should:

- Check if the article exists before deleting.
- Return a clear 404 error if the article cannot be found.

---

# Bug Summary

| Bug ID | Issue | Severity | Status |
|--------|-------|----------|--------|
| BUG-001 | GET article by ID causes server error | High | Open |
| BUG-002 | Invalid delete request response issue | Medium | Open |

---

# Conclusion

Backend testing identified issues affecting API reliability and user functionality.

All discovered bugs have been documented with reproduction steps and expected behaviour to help developers resolve them before deployment.