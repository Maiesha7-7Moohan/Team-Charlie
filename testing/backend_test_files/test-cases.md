# Backend Test Cases

## Project

**Project:** Web Scraping Analytics Dashboard

**Team:** Team Charlie

**Sprint:** Sprint 4

**Tester:** Angela Solomons

---

# Purpose

The purpose of this document is to record backend test cases used to verify API functionality, data processing, database communication, scraper functionality, and error handling.

Each test case defines the expected behaviour and the actual result observed during testing.

---

# Test Environment

| Item | Details |
|------|---------|
| Operating System | Windows 11 |
| Backend Framework | Flask |
| Programming Language | Python 3.14 |
| Database | MySQL |
| API Testing Tool | Postman |
| Frontend Framework | Vue.js |

---

# Backend Functional Test Cases

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-B001 | Server Startup | Verify Flask server starts successfully | Run Flask application | Server starts without errors | | |
| TC-B002 | Health Check | Verify API health endpoint works | Send GET request to /api/health | Returns 200 response | | |
| TC-B003 | Health Check | Verify unsupported method handling | Send POST request to /api/health | Returns 405 Method Not Allowed | | |
| TC-B004 | Items API | Retrieve all articles | Send GET request to /api/items | Returns article list in JSON format | | |
| TC-B005 | Items API | Retrieve single article by ID | Send GET request to /api/items/1 | Returns selected article | | |
| TC-B006 | Items API | Request article with invalid ID | Send GET request to /api/items/9999 | Returns 404 Not Found | | |
| TC-B007 | Items API | Request article using missing ID | Send GET request without ID | Returns validation error | | |
| TC-B008 | Search API | Search using valid keyword | Send GET request /api/search?q=python | Returns matching articles | | |
| TC-B009 | Search API | Search using unknown keyword | Send GET request /api/search?q=randomtext | Returns empty result list | | |
| TC-B010 | Search API | Search without query parameter | Send GET request /api/search | Returns validation message | | |

---

# CRUD Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-B011 | Create Data | Create new article record | Send POST request with valid JSON | Article created successfully | | |
| TC-B012 | Create Data | Create article with missing fields | Send POST request without required data | Returns 400 Bad Request | | |
| TC-B013 | Create Data | Submit invalid JSON format | Send malformed JSON request | Returns validation error | | |
| TC-B014 | Update Data | Update existing article | Send PUT request with valid ID | Article updated successfully | | |
| TC-B015 | Update Data | Update missing article | Send PUT request with invalid ID | Returns 404 error | | |
| TC-B016 | Delete Data | Delete existing article | Send DELETE request | Article removed successfully | | |
| TC-B017 | Delete Data | Delete missing article | Send DELETE request with invalid ID | Returns 404 error | | |

---

# Scraper Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-B018 | BBC Scraper | Run BBC scraper | Execute scraper script | Articles retrieved successfully | | |
| TC-B019 | CNN Scraper | Run CNN scraper | Execute scraper script | Articles retrieved successfully | | |
| TC-B020 | TechCrunch Scraper | Run TechCrunch scraper | Execute scraper script | Articles retrieved successfully | | |
| TC-B021 | CoinDesk Scraper | Run CoinDesk scraper | Execute scraper script | Articles retrieved successfully | | |
| TC-B022 | Scraper Data | Verify article fields | Inspect scraped output | Title, description and URL exist | | |
| TC-B023 | Scraper Data | Check duplicate articles | Run scraper twice | Duplicate handling works correctly | | |
| TC-B024 | Scraper Failure | Test scraper when website unavailable | Disconnect source website | Error handled correctly | | |

---

# Database Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-B025 | Database Connection | Verify database connection | Start backend application | Database connects successfully | | |
| TC-B026 | Data Storage | Verify scraped data saved | Run scraper and check database | Records stored correctly | | |
| TC-B027 | Data Retrieval | Retrieve stored articles | Call items endpoint | Stored records returned | | |
| TC-B028 | Database Error | Test unavailable database | Stop database service | Application returns controlled error | | |
| TC-B029 | Data Integrity | Verify required fields | Check database records | Required columns populated | | |

---

# API Validation Testing

| Test ID | Feature | Test Scenario | Expected Result | Actual Result | Status |
|---------|---------|---------------|-----------------|---------------|--------|
| TC-B030 | API Response | Validate JSON response format | Valid JSON returned | | |
| TC-B031 | API Response | Validate response fields | Required fields included | | |
| TC-B032 | API Status Codes | Verify successful requests | Correct 200/201 codes returned | | |
| TC-B033 | API Status Codes | Verify invalid requests | Correct 400/404 codes returned | | |
| TC-B034 | API Errors | Verify server errors handled | Controlled 500 response returned | | |

---

# Security Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-B035 | SQL Injection | Test malicious query input | Send SQL injection payload | Request safely rejected | | |
| TC-B036 | Input Validation | Submit empty fields | Send incomplete request | Validation error returned | | |
| TC-B037 | Invalid Data | Submit incorrect data types | Send invalid values | Request rejected | | |
| TC-B038 | Endpoint Security | Access invalid route | Request unknown endpoint | 404 returned | | |

---

# Performance Testing

| Test ID | Feature | Test Scenario | Expected Result | Actual Result | Status |
|---------|---------|---------------|-----------------|---------------|--------|
| TC-B039 | Items Endpoint | Retrieve all articles | Response under 3 seconds | | |
| TC-B040 | Search Endpoint | Search articles | Response under 2 seconds | | |
| TC-B041 | Statistics Endpoint | Load statistics data | Response under 2 seconds | | |
| TC-B042 | Scraper Endpoint | Run scrape request | Completes successfully | | |

---

# Regression Testing

| Test ID | Feature | Previous Issue | Expected Result | Status |
|---------|---------|----------------|-----------------|--------|
| TC-B043 | Items API | Article ID error fixed | Endpoint still returns correct data | |
| TC-B044 | Search API | Search validation changes | Search still works correctly | |
| TC-B045 | Scrapers | Parser fixes | Scrapers continue working | |

---

# Test Summary

| Metric | Count |
|--------|------:|
| Total Test Cases | 45 |
| Passed | |
| Failed | |
| Blocked | |

---

# Notes

All failed test cases must be recorded in the backend bug report document with:

- Bug ID
- Severity
- Steps to reproduce
- Expected behaviour
- Actual behaviour
- Evidence screenshots