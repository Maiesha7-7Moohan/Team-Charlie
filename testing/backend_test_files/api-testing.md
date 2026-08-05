# Backend API Testing

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |
| Testing Tool | Postman |

---

# Purpose

The purpose of API testing is to check that the backend communicates correctly with the frontend and other services.

This testing verifies that:

- API endpoints respond correctly
- Correct HTTP status codes are returned
- Data is returned in the correct format
- Invalid requests are handled properly
- Errors do not crash the application

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Backend Framework | Flask |
| Programming Language | Python |
| Database | MySQL |
| API Tool | Postman |
| API Base URL | http://127.0.0.1:5000/api |

---

# HTTP Status Codes Used

| Status Code | Meaning | When It Is Used |
|-------------|---------|----------------|
| 200 | OK | Request completed successfully |
| 201 | Created | New data was created successfully |
| 400 | Bad Request | User sent invalid information |
| 404 | Not Found | Requested item does not exist |
| 405 | Method Not Allowed | Wrong HTTP method used |
| 500 | Server Error | Backend failed unexpectedly |

---

# API Endpoint Test Results

## Articles Endpoint

| Test ID | Endpoint | Method | Expected Result | Actual Result | Status | Notes |
|---------|----------|--------|-----------------|---------------|--------|------|
| API-001 | /api/items | GET | Return all articles | | | |
| API-002 | /api/items/{id} | GET | Return one article | | | |
| API-003 | /api/items/9999 | GET | Return 404 for missing article | | | |

---

## Search Endpoint

| Test ID | Endpoint | Method | Expected Result | Actual Result | Status | Notes |
|---------|----------|--------|-----------------|---------------|--------|------|
| API-004 | /api/search?q=python | GET | Return matching articles | | | |
| API-005 | /api/search?q=random | GET | Return empty results | | | |
| API-006 | /api/search | GET | Return validation message | | | |

---

## Health Check Endpoint

| Test ID | Endpoint | Method | Expected Result | Actual Result | Status | Notes |
|---------|----------|--------|-----------------|---------------|--------|------|
| API-007 | /api/health | GET | Confirm server is running | | | |
| API-008 | /api/health | POST | Reject unsupported method | | | |

---

## Scraper Endpoint

| Test ID | Endpoint | Method | Expected Result | Actual Result | Status | Notes |
|---------|----------|--------|-----------------|---------------|--------|------|
| API-009 | /api/scrape | POST | Start scraping process | | | |
| API-010 | /api/scrape | POST | Reject invalid request | | | |

---

# Response Validation

For each API request, the following checks were performed.

| Check | Result | Notes |
|-------|--------|------|
| Response uses JSON format | | |
| Response contains expected fields | | |
| Status code is correct | | |
| Error messages are clear | | |
| Response time is acceptable | | |

---

# API Error Testing

The backend was tested using invalid requests to confirm that errors are handled correctly.

| Test | Expected Behaviour | Actual Behaviour | Status |
|------|--------------------|------------------|--------|
| Invalid article ID | Return 404 error | | |
| Missing required data | Return 400 error | | |
| Invalid endpoint | Return 404 error | | |
| Wrong HTTP method | Return 405 error | | |
| Database failure | Return controlled error | | |

---

# Postman Evidence

Screenshots should be saved for important API tests.

Recommended folder:

```
testing/
└── backend/
    └── screenshots/
        ├── API-001-items.png
        ├── API-002-item-id.png
        ├── API-003-invalid-id.png
        └── API-007-health.png
```

Each screenshot should show:

- Request URL
- HTTP method
- Response status code
- Response body

---

# Known Issues Found During Testing

| Bug ID | Endpoint | Issue | Severity | Status |
|--------|----------|-------|----------|--------|
| BUG-001 | /api/items/{id} | Server returns 500 error when requesting article by ID | High | Open |
| | | | | |

---

# API Testing Summary

| Metric | Number |
|--------|-------:|
| Total API Tests | 10 |
| Passed | |
| Failed | |
| Blocked | |

---

# Conclusion

API testing was completed to verify that the backend services work correctly and communicate properly.

The testing covered:

- API endpoints
- Status codes
- JSON responses
- Error handling
- Invalid requests
- Backend reliability

Any failed tests have been recorded as bugs and should be reviewed by the development team before release.