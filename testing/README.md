# QA Testing Documentation

## Project

**Project:** Web Scraping Analytics Dashboard  
**Team:** Team Charlie  
**Sprint:** Sprint 4  
**QA Tester:** Angela Solomons  

---

# Purpose of This Folder

The purpose of this folder is to store all Quality Assurance (QA) documentation for the Web Scraping Analytics Dashboard.

The documents inside this folder help the team:

- Plan testing activities
- Record test results
- Report bugs
- Track fixes
- Confirm application quality before release

---

# Testing Structure

The testing folder is divided into three main sections:

```
testing/

├── backend/
│
├── frontend/
│
├── reports/
│
└── screenshots/
```

---

# Backend Testing

Location:

```
testing/backend/
```

Backend QA focuses on testing the server-side functionality of the application.

This includes:

- Flask API
- Database communication
- Web scrapers
- Search functionality
- Data processing
- Error handling

---

## Backend Documents

### test-plan.md

Purpose:

Defines the overall backend testing approach.

Contains:

- Testing objectives
- Testing scope
- Tools used
- Testing responsibilities
- Risks

Use this document before starting backend testing.

---

### test-cases.md

Purpose:

Contains the detailed backend testing checklist.

Used for testing:

- API endpoints
- Database functions
- Scrapers
- Error handling
- Validation

During testing, update:

- Actual Result
- Status
- Notes

---

### api-testing.md

Purpose:

Records API testing performed using Postman.

Contains:

- Endpoint tests
- HTTP methods
- Status codes
- Response validation
- API evidence

Use screenshots from Postman as supporting evidence.

---

### bug-reports.md

Purpose:

Records backend problems discovered during testing.

Every bug should include:

- Bug ID
- Description
- Steps to reproduce
- Expected result
- Actual result
- Severity
- Evidence

---

### smoke-testing.md

Purpose:

A quick check to confirm the backend is working before detailed testing begins.

Checks:

- Server startup
- API availability
- Database connection
- Main functionality

---

### regression.md

Purpose:

Ensures that fixes and updates do not break existing backend functionality.

Used after:

- Bug fixes
- API changes
- Database updates

---

# Frontend Testing

Location:

```
testing/frontend/
```

Frontend QA focuses on the user-facing application.

This includes:

- Vue.js pages
- Navigation
- UI components
- Search
- Charts
- User interactions
- Responsive design

---

## Frontend Documents

### test-plan.md

Purpose:

Defines the frontend testing approach.

Contains:

- Testing scope
- Objectives
- Testing types
- Environment details

---

### test-cases.md

Purpose:

Contains frontend functionality tests.

Used for testing:

- Pages
- Buttons
- Search
- Navigation
- Data display
- User interactions

---

### ui-testing.md

Purpose:

Tests the visual appearance of the application.

Checks:

- Layout
- Colours
- Fonts
- Spacing
- Alignment
- Responsive design

---

### bug-reports.md

Purpose:

Records frontend issues.

Examples:

- Broken buttons
- Incorrect data display
- Layout problems
- Missing error messages

---

### smoke-testing.md

Purpose:

Quickly verifies that the frontend is usable.

Checks:

- Application loading
- Navigation
- Main features
- API connection

---

### regression.md

Purpose:

Confirms that frontend changes have not broken existing features.

Used after:

- UI updates
- Bug fixes
- New features

---

# Reports

Location:

```
testing/reports/
```

Reports combine all QA information into a summary for the team.

---

## sprint-summary.md

Purpose:

Provides a short overview of testing completed during a sprint.

Includes:

- Tests completed
- Bugs found
- Current status
- Testing progress

Audience:

- Scrum Master
- Team Lead
- Developers

---

## QA-Report_Summary.md

Purpose:

Provides the final QA assessment before release.

Includes:

- Testing coverage
- Defect summary
- Risks
- Release recommendation

---

# Screenshots and Evidence

Location:

```
testing/screenshots/
```

Screenshots provide proof of testing.

Examples:

- Postman responses
- Error messages
- UI problems
- Failed test cases

Recommended naming:

```
API-001-items-response.png

BUG-F001-layout-error.png

SM-F001-loading-screen.png
```

Good screenshots should show:

- The feature being tested
- The result
- Any error messages
- Relevant information

---

# QA Testing Workflow

Follow this order when testing a new build:

## Step 1: Smoke Testing

First confirm the application works.

Complete:

- Backend smoke testing
- Frontend smoke testing

If smoke testing fails, report critical issues before continuing.

---

## Step 2: Functional Testing

Execute:

- Backend test cases
- Frontend test cases

Record:

- Pass
- Fail
- Blocked

---

## Step 3: API Testing

Use Postman to verify:

- Endpoints
- Requests
- Responses
- Status codes

Save evidence screenshots.

---

## Step 4: Report Bugs

For failed tests:

1. Create a bug report.
2. Assign severity.
3. Add reproduction steps.
4. Attach evidence.

---

## Step 5: Regression Testing

After fixes:

- Retest the failed functionality.
- Confirm existing features still work.

---

## Step 6: Final QA Report

Update:

- Sprint summary
- Final report
- Test results

Provide QA recommendation.

---

# Bug Severity Guide

| Severity | Description |
|----------|-------------|
| Critical | Application cannot be used |
| High | Important feature is broken |
| Medium | Feature works with problems |
| Low | Minor issue or cosmetic problem |

---

# Test Result Guide

| Status | Meaning |
|--------|---------|
| Pass | Feature works as expected |
| Fail | Feature does not meet requirements |
| Blocked | Testing cannot continue due to another issue |
| Not Tested | Testing has not started |

---

# QA Responsibilities

QA is responsible for:

- Creating test documentation
- Executing tests
- Recording results
- Reporting bugs
- Providing evidence
- Confirming fixes

QA is not responsible for:

- Fixing code
- Changing requirements
- Approving developer changes

---

# Conclusion

This QA documentation structure provides a clear testing process for the Web Scraping Analytics Dashboard.

The documentation ensures that:

- Testing is organised
- Bugs are tracked properly
- Results are recorded
- The application quality can be measured before release