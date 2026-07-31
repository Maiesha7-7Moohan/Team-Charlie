# QA Progress Tracker

## Project Information

| Item | Details |
|------|---------|
| Project | News & Media Scraping Dashboard |
| Frontend QA Tester | Nuriyah Davids |
| Backend QA Tester | Angela Solomons |
| Repository | Team-Charlie |
| Current Branch | develop |
| Last Updated | 31 July 2026 |

---

# Overall Testing Progress

| Phase | Status |
|---------|---------|
| Smoke Testing | Phase 1 Completed |
| Frontend Testing | Phase 1 Completed |
| Backend Testing | Phase 1 Completed |
| API Testing | Phase 1 Completed |
| Integration Testing | ⬜ Not Started |
| Regression Testing | ⬜ Not Started |
| Final QA Review | ⬜ Not Started |

---

# Branch Testing Status

| Branch | Feature | Ready for Testing | Tested | Bugs Found | Retested | Status |
|---------|----------|------------------|---------|------------|----------|--------|
| feature/dashboard | Dashboard | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/search | Search | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/filter | Filters | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/articles | Articles | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/api | Flask API | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/parser | Data Parsing | ⬜ | ⬜ | 0 | ⬜ | Waiting |
| feature/scraper | Web Scraper | ⬜ | ⬜ | 0 | ⬜ | Waiting |

---

# Current Bugs

| Bug ID | Feature | Severity | Status |
|----------|---------|----------|--------|
| None | - | - | - |

---

# Testing Notes

| Date | Notes |
|------|-------|
| | |

---

# Next Actions

- [ ] Complete Smoke Testing
- [ ] Test Dashboard
- [ ] Test Navigation
- [ ] Test Search
- [ ] Test Filters
- [ ] Test Articles
- [ ] Test API
- [ ] Test Integration
- [ ] Perform Regression Testing



# QA Progress Tracker

## Project Information

| Item | Details |
|------|---------|
| Project | News & Media Scraping Dashboard |
| QA Lead | Angela Solomons |
| Frontend QA Tester | Nuriyah |
| Team | Team Charlie |
| Current Focus | feature/parsing complete |
| Last Updated | July 29, 2026 |

---

# Overall Testing Progress

| Phase | Status | Notes |
|---------|---------|-------|
| Backend Parsing (`feature/parsing`) | ☑ Complete | All 4 scrapers verified & signed off |
| Aggregator Testing (`feature/webscraping`) | ⬜ Not Started | Pending developer PR |
| API Testing (`feature/api`) | ⬜ Not Started | Pending developer PR |
| Frontend Smoke & UI (`feature/dashboard`) | ⬜ Not Started | Waiting for Vue dashboard build |
| Integration Testing | ⬜ Not Started | Dummy layout ready |
| Final QA Review | ⬜ Not Started | Waiting on develop merge |

---

# Branch Testing Status

| Branch | Feature | Ready for Testing | Tested | Bugs Found | Retested | Status |
|---------|----------|------------------|---------|------------|----------|--------|
| feature/parsing | Data Parsing / Scrapers | ☑ | ☑ | 2 | ☑ | PASSED |
| feature/webscraping | Web Scraper Orchestration | ⬜ | ⬜ | 0 | 0 | Waiting |
| feature/api | Flask API | ⬜ | ⬜ | 0 | 0 | Waiting |
| feature/dashboard | Dashboard UI | ⬜ | ⬜ | 0 | 0 | Waiting |
| feature/search | Search Functionality | ⬜ | ⬜ | 0 | 0 | Waiting |
| feature/filter | Category Filters | ⬜ | ⬜ | 0 | 0 | Waiting |
| feature/articles | Article Display | ⬜ | ⬜ | 0 | 0 | Waiting |

---

# Bug History Log

| Bug ID | Feature / File | Severity | Reported By | Status | Resolution |
|----------|----------------|----------|-------------|--------|------------|
| BUG-001 | `cnn_scrapper.py` | High | Angela Solomons | Closed | Added missing `requests` import |
| BUG-002 | `cnn_scrapper.py` | Medium | Angela Solomons | Closed | Replaced dynamic CSS hashes with OpenGraph tags |
| BUG-003 | `app.py` | High | Angela Solomons | Closed | Fixed incorrect HTTP status code from `40` to `404` |

---

# QA Execution Log

| Date | Activity / Notes |
|------|------------------|
| July 29, 2026 | Tested `feature/parsing` scripts (`coindesk`, `bbc`, `techcrunch`, `cnn`). Logged `BUG-001` & `BUG-002`. Verified fixes pushed by Zanda. Scrapers 100% passed. |
| July 29, 2026 | Established QA file structures, bug report layouts, and dashboard test case templates for upcoming frontend review. |
| July 30, 2026 | Completed backend testing for api endpoints, logged bug report. |

---

# Next Actions

- [x] Receive notice when backend branches are merged and ready for Phase 2 testing.
- [ ] Receive notice when Khanya's `feature/webscraping` aggregator is ready for testing
- [ ] Receive notice when Karah's `feature/api` endpoints are ready
- [ ] Run smoke test and UI test suite on Nuriyah's `feature/dashboard` when pushed