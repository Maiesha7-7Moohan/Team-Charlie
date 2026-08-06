# Backend Smoke Testing

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |

---

# Purpose

The purpose of smoke testing is to quickly verify that the backend is stable enough for further testing.

Smoke testing checks that:

- The Flask server starts
- Main API endpoints are available
- Basic requests work
- The backend does not have major failures

If smoke testing fails, detailed testing should stop until the main issues are fixed.

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Backend Framework | Flask |
| Language | Python |
| Database | MySQL |
| API Testing Tool | Postman |
| API URL | http://127.0.0.1:5000/api |

---

# Smoke Test Checklist

| Test ID | Test Area | Test Description | Expected Result | Actual Result | Status |
|---------|-----------|------------------|-----------------|---------------|--------|
| SM-B001 | Server | Start Flask backend | Server starts without errors | | |
| SM-B002 | Health Check | Send GET request to /api/health | API returns 200 OK | | |
| SM-B003 | Articles API | Send GET request to /api/items | Articles are returned | | |
| SM-B004 | Single Article | Send GET request to /api/items/1 | Article details returned | | |
| SM-B005 | Search | Send GET request to /api/search?q=python | Search results returned | | |
| SM-B006 | Database | Verify backend connects to database | Database connection successful | | |
| SM-B007 | Scraper | Run scraper manually | Articles are collected successfully | | |
| SM-B008 | Error Handling | Send request to invalid endpoint | 404 response returned | | |

---

# Smoke Test Results

| Result | Number |
|--------|-------:|
| Total Tests | 8 |
| Passed | |
| Failed | |
| Blocked | |

---

# Failed Smoke Tests

If any smoke test fails, record it below.

| Test ID | Issue | Bug ID | Status |
|---------|-------|--------|--------|
| | | | |

---

# Testing Notes

During smoke testing, confirm:

### Backend Server

- Flask starts correctly
- No startup errors appear
- Required packages are installed

### API

- Endpoints respond
- Correct status codes are returned
- Responses contain valid JSON

### Database

- Connection works
- Data can be retrieved

### Scrapers

- Scraper files execute
- Articles are returned correctly

---

# Conclusion

Smoke testing provides a quick check that the backend is working before deeper testing begins.

The backend is ready for full testing when:

- The server starts successfully
- Main API endpoints respond correctly
- No critical failures prevent testing