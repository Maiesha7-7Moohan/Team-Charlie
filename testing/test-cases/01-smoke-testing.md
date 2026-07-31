# Smoke Testing

## Project

News & Media Scraping Dashboard

---

## Purpose

The purpose of Smoke Testing is to verify that the application is stable enough for further functional testing.

Smoke Testing is performed on every new feature branch before detailed testing begins.

---

## Test Environment

| Item | Value |
|------|-------|
| Operating System | Windows 11 |
| Browser | Google Chrome |
| Frontend | Vue.js + Vite |
| Backend | Flask |
| API Client | Axios |
| Testing Tool | Postman |
| Version | Development |

---

# Smoke Test Cases

---

## ST-001

### Test Name

Verify project can be cloned successfully.

### Preconditions

Repository exists.

### Steps

1. Clone repository.
2. Open project in VS Code.

### Expected Result

Repository clones successfully.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-002

### Test Name

Verify frontend dependencies install.

### Preconditions

Node.js installed.

### Steps

1. Open frontend folder.
2. Run

```bash
npm install
```

### Expected Result

Dependencies install successfully without blocking errors.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-003

### Test Name

Verify Vue application starts.

### Preconditions

Dependencies installed.

### Steps

Run

```bash
npm run dev
```

### Expected Result

Vite starts successfully.

A localhost URL is displayed.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-004

### Test Name

Verify application loads in browser.

### Preconditions

Vue running.

### Steps

1. Open localhost.
2. Wait for Dashboard.

### Expected Result

Application loads without errors.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-005

### Test Name

Verify browser console contains no critical errors.

### Preconditions

Application running.

### Steps

1. Press F12.
2. Open Console.

### Expected Result

No uncaught JavaScript errors.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-006

### Test Name

Verify backend starts.

### Preconditions

Python installed.

### Steps

Activate virtual environment.

Run Flask.

### Expected Result

Backend starts successfully.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-007

### Test Name

Verify API responds.

### Preconditions

Backend running.

### Steps

Open Postman.

Call an endpoint.

### Expected Result

HTTP 200 response.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-008

### Test Name

Verify JSON data exists.

### Preconditions

Backend configured.

### Steps

Locate JSON data.

### Expected Result

JSON file exists and is valid.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## ST-009

### Test Name

Verify frontend receives data.

### Preconditions

Backend running.

### Steps

Refresh Dashboard.

### Expected Result

Articles appear successfully.

### Actual Result



### Status

⬜ PASS

⬜ FAIL

### Notes



---

## Smoke Test Summary

| Test ID | Result |
|----------|--------|
| ST-001 | |
| ST-002 | |
| ST-003 | |
| ST-004 | |
| ST-005 | |
| ST-006 | |
| ST-007 | |
| ST-008 | |
| ST-009 | |

---

## Smoke Test Outcome

☐ PASS

☐ FAIL

---

## QA Comments
