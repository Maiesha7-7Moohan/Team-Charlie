# Frontend Regression Testing

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |
| Testing Type | Frontend Regression Testing |

---

# Purpose

The purpose of regression testing is to confirm that updates, changes, and bug fixes have not broken existing frontend functionality.

Regression testing focuses on retesting important features that were already working.

---

# When Regression Testing Is Performed

Regression testing should be completed after:

- Frontend code changes
- UI updates
- Bug fixes
- New features are added
- Backend API changes affect the frontend

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Browser | Google Chrome |
| Frontend Framework | Vue.js |
| Backend Connection | Flask API |
| Testing Method | Manual Testing |

---

# Regression Test Cases

| Test ID | Feature | Test Description | Expected Result | Actual Result | Status |
|---------|---------|------------------|-----------------|---------------|--------|
| REG-F001 | Application Load | Open application after updates | Website loads correctly | | |
| REG-F002 | Navigation | Test all menu links | All pages open correctly | | |
| REG-F003 | Dashboard | Verify dashboard display | Dashboard still works | | |
| REG-F004 | Articles | Verify article list | Articles display correctly | | |
| REG-F005 | Search | Test search after changes | Search still returns results | | |
| REG-F006 | Statistics | Verify charts and data | Statistics display correctly | | |
| REG-F007 | Buttons | Test interactive elements | Buttons work correctly | | |
| REG-F008 | Responsive Design | Resize browser | Layout remains usable | | |
| REG-F009 | Error Handling | Test API failure handling | Error messages display correctly | | |
| REG-F010 | Browser Refresh | Refresh application pages | No data or layout issues occur | | |

---

# Bug Fix Regression Testing

Previously reported bugs should be retested after developers provide a fix.

---

# BUG-F001 Regression Test

## Issue

Article details were not displaying correctly.

## Fix To Verify

Confirm that:

- Article data loads correctly
- All fields display properly
- No missing information appears

| Test ID | Test | Expected Result | Actual Result | Status |
|---------|------|-----------------|---------------|--------|
| REG-F011 | Open article details | Article information displays correctly | | |

---

# BUG-F002 Regression Test

## Issue

Frontend did not display an error message when the backend API was unavailable.

## Fix To Verify

Confirm that:

- API failures are detected
- Users receive a clear message
- Application does not crash

| Test ID | Test | Expected Result | Actual Result | Status |
|---------|------|-----------------|---------------|--------|
| REG-F012 | Disable backend connection | Error message displays correctly | | |

---

# Responsive Regression Testing

After frontend changes, verify the application still works on different screen sizes.

| Test ID | Device | Expected Result | Actual Result | Status |
|---------|--------|-----------------|---------------|--------|
| REG-F013 | Desktop | Layout displays correctly | | |
| REG-F014 | Laptop | Content fits screen | | |
| REG-F015 | Mobile | Components adjust correctly | | |

---

# Regression Test Summary

| Metric | Count |
|--------|------:|
| Total Regression Tests | 15 |
| Passed | |
| Failed | |
| Blocked | |

---

# Regression Testing Notes

During regression testing, QA should verify:

## User Interface

- Layout has not changed unexpectedly
- Buttons still work
- Styling remains consistent

## Data Display

- API data still appears correctly
- Tables and charts still load

## Navigation

- Routes still work
- Pages open correctly

## User Experience

- Error messages are clear
- Loading states work
- Application remains easy to use

---

# Conclusion

Frontend regression testing ensures that new updates and fixes improve the application without causing new problems.

Any failed regression tests should be recorded in the frontend bug reports and reviewed before release.