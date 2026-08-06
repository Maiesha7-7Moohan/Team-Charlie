# Backend Regression Testing

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |

---

# Purpose

The purpose of regression testing is to confirm that new changes, bug fixes, or updates have not broken existing backend functionality.

Regression testing focuses on previously tested features to ensure the application remains stable.

---

# When Regression Testing Is Performed

Regression testing should be completed after:

- Bug fixes are implemented
- API endpoints are changed
- Database changes are made
- Scraper logic is updated
- New backend features are added

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Backend Framework | Flask |
| Programming Language | Python |
| Database | MySQL |
| Testing Tool | Postman |

---

# Regression Test Cases

| Test ID | Feature | Test Description | Expected Result | Actual Result | Status |
|---------|---------|------------------|-----------------|---------------|--------|
| REG-B001 | Health Endpoint | Verify backend health check after changes | Returns 200 OK | | |
| REG-B002 | Items Endpoint | Verify all articles can still be retrieved | Returns article list | | |
| REG-B003 | Article Details | Verify single article retrieval works | Returns article data | | |
| REG-B004 | Search | Verify search still returns results | Matching articles displayed | | |
| REG-B005 | Invalid Search | Verify empty search results are handled | Empty result returned correctly | | |
| REG-B006 | Scrapers | Verify scrapers still collect data | Articles retrieved successfully | | |
| REG-B007 | Database | Verify database records are unchanged | Data remains correct | | |
| REG-B008 | Error Handling | Verify invalid requests still return errors | Correct error codes returned | | |

---

# Bug Fix Regression Testing

These tests are linked to previously discovered bugs.

---

## BUG-001 Regression Test

### Issue

GET `/api/items/{id}` returned a 500 Internal Server Error.

### Fix To Verify

Developer should ensure:

- Articles contain a valid ID field
- Missing articles return 404
- API no longer crashes

---

| Test ID | Test | Expected Result | Actual Result | Status |
|---------|------|-----------------|---------------|--------|
| REG-B009 | GET /api/items/1 | Returns article with 200 status | | |
| REG-B010 | GET /api/items/9999 | Returns 404 error | | |

---

## BUG-002 Regression Test

### Issue

DELETE request for an invalid article did not return the expected response.

### Fix To Verify

Developer should ensure:

- Existing articles can be deleted
- Missing articles return a clear 404 response

---

| Test ID | Test | Expected Result | Actual Result | Status |
|---------|------|-----------------|---------------|--------|
| REG-B011 | Delete existing article | Article deleted successfully | | |
| REG-B012 | Delete invalid article | Returns 404 error | | |

---

# Regression Test Summary

| Metric | Count |
|--------|------:|
| Total Regression Tests | 12 |
| Passed | |
| Failed | |
| Blocked | |

---

# Regression Testing Notes

During regression testing, QA should verify:

### API

- Existing endpoints still work
- Status codes have not changed unexpectedly
- Response formats remain consistent

### Database

- Data is not lost
- Records remain accurate
- Database operations still work

### Scrapers

- Scrapers still collect articles
- Data structure remains unchanged

### Error Handling

- Invalid requests are handled correctly
- Backend does not crash

---

# Conclusion

Regression testing confirms that backend improvements and bug fixes do not negatively affect existing functionality.

All failed regression tests should be linked to a bug report and reviewed before release approval.