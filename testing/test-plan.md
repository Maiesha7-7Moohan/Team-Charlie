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