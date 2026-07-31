# Test Plan
## News & Media Scraping Dashboard

---

## 1. Document Information

| Item | Description |
|------|-------------|
| Project | News & Media Scraping Dashboard |
| QA Tester | Angela Solomons |
| Team | Team Charlie |
| Version | 1.0 |
| Date | July 2026 |
| Environment | Development |

---

# 2. Introduction

This document describes the testing strategy for the News & Media Scraping Dashboard.

The purpose of testing is to verify that all frontend and backend functionality performs according to the project requirements before the application is merged into the main branch.

Testing will be performed throughout the Agile development process as features become available.

---

# 3. Objectives

The objectives of testing are to:

- Verify that each feature functions correctly.
- Verify that frontend and backend components communicate correctly.
- Verify that scraped data is correctly parsed and displayed.
- Identify functional defects before release.
- Verify system stability after integration.

---

# 4. Scope

The following features are included in testing.

## Frontend

- Dashboard
- Navigation
- Search
- Filters
- Article List
- Article Details
- Error Messages
- Loading States

## Backend

- Flask API
- JSON responses
- Data parsing
- Scraper output
- Error handling

---

# 5. Testing Types

The following testing activities will be performed.

- Smoke Testing
- Functional Testing
- API Testing
- Integration Testing
- Regression Testing
- UI Testing
- JSON Validation

---

# 6. Test Environment

Operating System

- Windows 11

Frontend

- Vue.js
- Vite

Backend

- Flask
- Python

Testing Tools

- Postman
- Google Chrome
- Chrome DevTools
- GitHub
- Git
- VS Code

---

# 7. Entry Criteria

Testing may begin when:

- Feature branch has been pushed.
- Project builds successfully.
- Required dependencies are installed.

---

# 8. Exit Criteria

Testing is complete when:

- All planned test cases have been executed.
- Critical defects have been resolved.
- Regression testing passes.
- Team approves merge into main.

---

# 9. Risks

Potential risks include:

- Incomplete feature branches.
- API endpoints unavailable.
- Missing JSON files.
- Merge conflicts.
- Inconsistent project structure.

---

# 10. Deliverables

The following QA documents will be produced.

- Test Plan
- Test Cases
- Progress Tracker
- QA Summary
- Screenshots
- Postman Collection





<!-- NEW -->
# Test Plan
## News & Media Scraping Dashboard

---

## 1. Document Information

| Item | Description |
|------|-------------|
| Project | News & Media Scraping Dashboard |
| QA Lead | Angela Solomons |
| Frontend QA Tester | Nuriyah |
| Team | Team Charlie |
| Version | 1.0 |
| Date | July 2026 |
| Environment | Development |

---

# 2. Introduction

This document describes the testing strategy for the News & Media Scraping Dashboard.

The purpose of testing is to verify that all frontend and backend functionality performs according to the project requirements before the application is merged into the main branch.

Testing will be performed throughout the Agile development process as features become available across dedicated feature branches.

---

# 3. Objectives

The objectives of testing are to:

- Verify that each feature functions correctly.
- Verify that frontend and backend components communicate correctly via Axios and Flask endpoints.
- Verify that scraped data is correctly parsed, deduplicated, stored, and displayed.
- Identify functional defects before release and document resolutions.
- Verify system stability after backend and frontend integration.

---

# 4. Scope

The following features are included in testing.

## Frontend (QA Lead: Angela Solomons | Frontend QA: Nuriyah)

- Dashboard
- Navigation
- Search
- Filters
- Article List
- Article Details
- Error Messages
- Loading States

## Backend (QA Lead: Angela Solomons)

- Flask API (`/api/items`, `/api/health`, `/api/search`)
- JSON responses & Schema Validation
- Data parsing (`feature/parsing`)
- Scraper output & Orchestration (`feature/webscraping`)
- Error handling & Rate Limiting

---

# 5. Testing Types

The following testing activities will be performed.

- Smoke Testing
- Functional Testing
- API Testing
- Integration Testing
- Regression Testing
- UI & Responsiveness Testing
- JSON Schema Validation

---

# 6. Test Environment

Operating System

- Windows 11

Frontend

- Vue.js
- Vite
- Axios

Backend

- Flask
- Python 3.x
- BeautifulSoup4
- Requests

Testing Tools

- Postman
- Google Chrome
- Chrome DevTools
- GitHub / Git
- VS Code

---

# 7. Entry Criteria

Testing may begin when:

- Feature branch has been pushed by developers.
- Project builds successfully without syntax or module errors.
- Required dependencies (`pip install -r requirements.txt`, `npm install`) are installed.

---

# 8. Exit Criteria

Testing is complete when:

- All planned test cases have been executed.
- Critical and High defects have been resolved and closed.
- Regression testing passes on `develop`.
- QA Team (Angela & Nuriyah) approves merge into main.

---

# 9. Risks

Potential risks include:

- Incomplete feature branches or unhandled edge cases.
- External target news sites rate-limiting or updating HTML structures.
- Missing or malformed JSON storage files.
- Integration merge conflicts between frontend and backend APIs.
- Inconsistent project key naming conventions.

---

# 10. Deliverables

The following QA documents will be produced.

- Test Plan
- Test Cases (Backend Scrapers & Frontend Dashboard)
- Progress Tracker
- QA Summary Reports
- Bug Reports
- Screenshots
- Postman Collection