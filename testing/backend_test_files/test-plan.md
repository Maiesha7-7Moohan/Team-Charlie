# Backend Test Plan

## Project

Web Scraping Analytics Dashboard

---

## Team

Team Charlie

---

## QA

Angela Solomons

---

## Sprint

Sprint 4 - Backend Testing

---

# Purpose

The purpose of this test plan is to verify that the Flask backend functions correctly, APIs return the expected responses, scraped data is stored correctly, and backend services remain stable throughout development.

Testing will focus on functionality, reliability, API correctness, data integrity, and regression testing.

---

# Scope

The following backend components are included in testing:

- Flask Application
- REST API Endpoints
- Web Scrapers
- Search Functionality
- Statistics Endpoint
- Scrape Now Endpoint
- JSON Data
- MySQL Database
- Error Handling
- CORS Configuration

---

# Objectives

The objectives of backend testing are:

- Verify every API endpoint returns the correct HTTP status code.
- Validate JSON response structure.
- Verify scraped data is cleaned correctly.
- Ensure MySQL stores retrieved data correctly.
- Validate search functionality.
- Verify statistics calculations.
- Confirm scrape jobs execute successfully.
- Identify defects before deployment.

---

# Test Types

## Smoke Testing

Verify that the backend starts successfully and critical endpoints respond.

---

## Functional Testing

Verify each endpoint performs its intended function.

---

## API Testing

Validate:

- Request methods
- Status codes
- Response bodies
- Error messages
- Invalid input handling

---

## Database Testing

Verify:

- Data insertion
- Duplicate handling
- Data retrieval
- Database consistency

---

## Regression Testing

Retest previously fixed defects to ensure they have not reappeared.

---

# Test Environment

Operating System

Windows 11

Python


Backend Framework

Flask

Database

MySQL

API Client

Postman

Browser

Google Chrome

Version Control

Git

Repository

GitHub

---

# Entry Criteria

Testing may begin once:

- Backend builds successfully
- Flask server starts
- API endpoints are available
- Database connection is established
- Scrapers execute successfully

---

# Exit Criteria

Testing is complete when:

- All critical tests pass
- High severity defects are resolved
- No blocker defects remain
- Regression testing passes
- QA approval is provided

---

# Risks

Potential risks include:

- Website structure changes causing scraper failures
- API downtime
- Database connection failures
- Invalid JSON data
- Network interruptions

---

# Deliverables

- Test Plan
- Test Cases
- API Test Results
- Bug Reports
- Regression Report
- Smoke Test Report
- Final QA Summary