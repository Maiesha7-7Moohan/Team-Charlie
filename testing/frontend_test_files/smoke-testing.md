# Frontend Smoke Testing

## Project Information

| Item | Details |
|------|---------|
| Project | Web Scraping Analytics Dashboard |
| Team | Team Charlie |
| Sprint | Sprint 4 |
| Tester | Angela Solomons |
| Testing Type | Frontend Smoke Testing |

---

# Purpose

The purpose of smoke testing is to quickly confirm that the frontend application is stable enough for detailed testing.

Smoke testing checks the most important features of the application:

- Application loading
- Navigation
- Main pages
- API connection
- Basic user interactions

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Browser | Google Chrome |
| Frontend Framework | Vue.js |
| Backend Framework | Flask |
| Testing Method | Manual Testing |

---

# Smoke Test Checklist

| Test ID | Feature | Test Description | Expected Result | Actual Result | Status |
|---------|---------|------------------|-----------------|---------------|--------|
| SM-F001 | Application Load | Open the website | Application loads successfully | | |
| SM-F002 | Page Rendering | Check homepage/dashboard | Main page displays correctly | | |
| SM-F003 | Navigation | Click navigation links | Pages open correctly | | |
| SM-F004 | API Connection | Load data from backend | Data displays correctly | | |
| SM-F005 | Articles | Open article section | Articles are visible | | |
| SM-F006 | Search | Use search feature | Search returns results | | |
| SM-F007 | Statistics | Open statistics section | Charts/data display correctly | | |
| SM-F008 | Buttons | Test main buttons | Buttons perform expected actions | | |
| SM-F009 | Error Handling | Disconnect backend | Error message appears | | |
| SM-F010 | Browser Refresh | Refresh application | Application reloads correctly | | |

---

# Smoke Test Execution

## Application Loading

Check:

- Vue application starts
- No blank pages appear
- No major console errors occur

Result:

| Check | Status |
|-------|--------|
| Application starts | |
| Components load | |
| No critical errors | |

---

## Navigation Check

Verify:

- All menu items work
- Correct pages open
- No broken routes exist

Result:

| Check | Status |
|-------|--------|
| Dashboard opens | |
| Articles page opens | |
| Statistics page opens | |
| Other pages open | |

---

## Data Loading Check

Verify:

- API requests complete
- Data appears correctly
- Loading indicators work

Result:

| Check | Status |
|-------|--------|
| Articles load | |
| Search works | |
| Statistics load | |

---

# Smoke Test Results

| Result | Count |
|--------|------:|
| Total Tests | 10 |
| Passed | |
| Failed | |
| Blocked | |

---

# Failed Smoke Tests

Record failed tests below.

| Test ID | Issue | Bug ID | Status |
|---------|-------|--------|--------|
| | | | |

---

# Evidence

Screenshots should be saved for failed or important smoke tests.

Recommended folder:

```
testing/
└── frontend/
    └── screenshots/
        ├── SM-F001-loading.png
        ├── SM-F004-api-data.png
        ├── SM-F006-search.png
        └── SM-F009-error.png
```

---

# Notes

Smoke testing should be completed:

- After receiving a new frontend build
- After major frontend changes
- Before full regression testing

---

# Conclusion

Smoke testing confirms that the frontend application is working at a basic level before detailed testing begins.

The application is ready for full testing when:

- Pages load successfully
- Navigation works
- Data displays correctly
- No critical issues prevent testing