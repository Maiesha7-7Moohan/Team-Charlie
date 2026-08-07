# Frontend Test Cases

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |
| Frontend Framework | Vue.js |

---

# Purpose

The purpose of this document is to record frontend test cases used to verify the application's user interface, user interactions, data display, and overall user experience.

Each test case includes:

- What is being tested
- How to test it
- Expected behaviour
- Actual result
- Test status

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Browser | Google Chrome |
| Frontend | Vue.js |
| Backend Connection | Flask API |
| Testing Type | Manual Testing |

---

# Application Loading Tests

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F001 | Application Load | Open website | Navigate to application URL | Website loads successfully | | |
| TC-F002 | Application Load | Refresh page | Refresh browser | Application reloads correctly | | |
| TC-F003 | Application Load | Check console errors | Open browser developer tools | No major errors displayed | | |
| TC-F004 | Loading Screen | Open application during loading | Load page | Loading indicator displays correctly | | |

---

# Navigation Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F005 | Navigation | Open dashboard page | Click dashboard link | Dashboard page opens | | |
| TC-F006 | Navigation | Move between pages | Click navigation links | Correct page opens | | |
| TC-F007 | Navigation | Active menu item | Open different pages | Current page is highlighted | | |
| TC-F008 | Navigation | Broken links | Click all navigation items | No broken links found | | |

---

# Dashboard Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F009 | Dashboard | View dashboard | Open dashboard | Dashboard loads correctly | | |
| TC-F010 | Dashboard | Check statistics cards | View summary information | Correct values displayed | | |
| TC-F011 | Dashboard | Check article count | Load dashboard data | Article count displays correctly | | |
| TC-F012 | Dashboard | Refresh dashboard data | Reload page | Data loads again correctly | | |

---

# Article Display Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F013 | Articles | View article list | Open articles section | Articles display correctly | | |
| TC-F014 | Articles | Check article titles | View article cards/table | Titles display correctly | | |
| TC-F015 | Articles | Check descriptions | Open article list | Descriptions display correctly | | |
| TC-F016 | Articles | Check article links | Click article link | Correct external page opens | | |
| TC-F017 | Articles | Empty data handling | Load page without articles | Empty state message displayed | | |

---

# Search Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F018 | Search | Search valid keyword | Enter "python" | Matching articles appear | | |
| TC-F019 | Search | Search invalid keyword | Enter random text | No results message appears | | |
| TC-F020 | Search | Empty search | Submit without text | Validation message appears | | |
| TC-F021 | Search | Clear search | Remove search text | Full results return | | |

---

# Statistics and Charts Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F022 | Statistics | Open statistics page | Navigate to statistics | Page loads correctly | | |
| TC-F023 | Charts | Check chart display | View charts | Charts render correctly | | |
| TC-F024 | Charts | Check chart data | Compare displayed values | Values match backend data | | |
| TC-F025 | Charts | Resize browser | Change window size | Charts remain usable | | |

---

# Error Handling Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F026 | API Error | Disable backend | Load application | Error message displayed | | |
| TC-F027 | API Error | Slow response | Simulate delay | Loading state shown | | |
| TC-F028 | Missing Data | Remove API data | Open page | Application handles missing data | | |

---

# Form and Button Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F029 | Buttons | Click buttons | Test all buttons | Buttons perform correct actions | | |
| TC-F030 | Search Button | Click search | Enter search and submit | Search executes successfully | | |
| TC-F031 | Reset Button | Click reset | Reset filters | Default state restored | | |

---

# Responsive Design Testing

| Test ID | Feature | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---------|---------|---------------|-------|-----------------|---------------|--------|
| TC-F032 | Desktop View | Test large screen | Open on desktop | Layout displays correctly | | |
| TC-F033 | Laptop View | Test laptop resolution | Resize browser | Content fits correctly | | |
| TC-F034 | Mobile View | Test mobile layout | Resize to mobile size | Responsive layout works | | |
| TC-F035 | Navigation Mobile | Open menu on mobile | Use mobile navigation | Menu works correctly | | |

---

# Browser Testing

| Test ID | Feature | Test Scenario | Expected Result | Actual Result | Status |
|---------|---------|---------------|-----------------|---------------|--------|
| TC-F036 | Chrome | Test application | Works correctly | | |
| TC-F037 | Browser Refresh | Refresh pages | No unexpected errors | | |
| TC-F038 | Developer Console | Check errors | No critical errors | | |

---

# Accessibility Testing

| Test ID | Feature | Test Scenario | Expected Result | Actual Result | Status |
|---------|---------|---------------|-----------------|---------------|--------|
| TC-F039 | Text | Check readability | Text is clear and readable | | |
| TC-F040 | Buttons | Check labels | Buttons have clear names | | |
| TC-F041 | Images | Check images/icons | Alt text available where needed | | |
| TC-F042 | Colours | Check contrast | Text is easy to read | | |

---

# Regression Testing

| Test ID | Feature | Test Scenario | Expected Result | Status |
|---------|---------|---------------|-----------------|--------|
| TC-F043 | Search | Retest after fixes | Search still works | |
| TC-F044 | Dashboard | Retest after updates | Dashboard still loads | |
| TC-F045 | Navigation | Retest after changes | Pages still open correctly | |

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

Any failed test case should be documented in the frontend bug report.

Include:

- Screenshot evidence
- Steps to reproduce
- Expected behaviour
- Actual behaviour
- Severity level