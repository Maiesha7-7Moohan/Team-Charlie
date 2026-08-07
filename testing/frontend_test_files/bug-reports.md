# Frontend Bug Reports

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |

---

# Purpose

The purpose of this document is to record all frontend issues discovered during testing.

Bug reports help developers understand:

- What went wrong
- How to reproduce the issue
- The expected behaviour
- The actual behaviour
- The impact on users

---

# Bug Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Application cannot be used |
| High | Important feature is broken |
| Medium | Feature works but has issues |
| Low | Small visual or usability issue |

---

# Bug List

| Bug ID | Title | Severity | Status |
|--------|-------|----------|--------|
| BUG-F001 | Article details do not display correctly | High | Open |
| BUG-F002 | Error message not displayed when API fails | Medium | Open |
| | | | |

---

# BUG-F001

## Title

Article details do not display correctly

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
| Frontend | Vue.js |
| Browser | Google Chrome |
| Page | Article Details |
| Backend API | Flask |

---

## Description

When a user selects an article, the article details page does not display the expected information.

The page either shows incomplete data or fails to load the article information.

---

## Steps to Reproduce

1. Open the dashboard application.
2. Navigate to the articles section.
3. Select an article.
4. View the article details page.

---

## Expected Result

The page should display:

- Article title
- Article description
- Source information
- Article link
- Other available details

---

## Actual Result

Article information does not display correctly.

The user cannot view the selected article details.

---

## Impact

Users are unable to access complete article information from the dashboard.

---

## Evidence

Screenshot:

```
testing/frontend/screenshots/BUG-F001-article-details.png
```

---

## Recommended Fix

Developer should:

- Check the API response mapping.
- Verify Vue components receive the correct data.
- Handle missing fields safely.

---

# BUG-F002

## Title

No error message displayed when backend API is unavailable

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
| Frontend | Vue.js |
| Browser | Google Chrome |
| Backend | Flask API |

---

## Description

When the backend API is unavailable, the frontend does not clearly inform the user that data could not be loaded.

---

## Steps to Reproduce

1. Stop the Flask backend server.
2. Open the frontend application.
3. Navigate to a page requiring API data.

---

## Expected Result

The application should display a clear message:

Example:

```
Unable to load data. Please try again later.
```

---

## Actual Result

The page remains blank or does not provide useful feedback.

---

## Impact

Users do not know whether the application is loading, broken, or experiencing a connection issue.

---

## Evidence

Screenshot:

```
testing/frontend/screenshots/BUG-F002-api-error.png
```

---

## Recommended Fix

Developer should:

- Add API error handling.
- Display user-friendly error messages.
- Provide retry options where necessary.

---

# Bug Summary

| Bug ID | Issue | Severity | Status |
|--------|-------|----------|--------|
| BUG-F001 | Article details display issue | High | Open |
| BUG-F002 | Missing API error message | Medium | Open |

---

# Bug Reporting Guidelines

Every new frontend bug should include:

- Unique bug ID
- Clear title
- Severity level
- Steps to reproduce
- Expected result
- Actual result
- Screenshot evidence
- Suggested fix

---

# Conclusion

Frontend testing identified issues affecting user experience and application usability.

All discovered issues should be reviewed, fixed, and retested before final release approval.