# Team Charlie – Web Scraping Analytics Dashboard

A full-stack web application that scrapes news articles from multiple online sources, processes and stores the data, and displays it through an interactive dashboard.

The project was developed using an Agile Scrum workflow. Development was completed collaboratively using Git feature branches, code reviews, testing, and staged merges into the shared development branch.

---

# Features

- Multi-source news article scraping
- Interactive Vue.js frontend
- Responsive user interface
- Article search and filtering
- Statistics dashboard
- Article management (CRUD)
- RESTful API built with Flask
- JSON-based data storage
- Automated backend testing
- Manual frontend and backend QA documentation

---

# Technology Stack

## Frontend

- Vue 3
- Vite
- Axios
- Three.js

## Backend

- Python
- Flask
- Flask-CORS
- BeautifulSoup4
- Requests
- lxml

## QA

- Postman
- GitHub
- Chrome DevTools
- Manual Testing
- Automated Python Tests
- Pytest

---

# Project Structure

```text
Team-Charlie/

├── backend/
│   ├── app.py
│   ├── routes/
│   ├── scrapers/
│   ├── data/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── testing/
│   ├── backend/
│   ├── frontend/
│   ├── reports/
│   └── screenshots/
│
└── README.md
```

---
# Installation

## Clone the repository

```bash
git clone https://github.com/Maiesha7-7Moohan/Team-Charlie.git

cd Team-Charlie
```

---

# Backend Setup

1. Open a terminal.

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Navigate to the backend folder:

```bash
cd backend
```

4. Start the Flask server:

```bash
python app.py
```

Backend will run at:

```
http://127.0.0.1:5000
```

---

# Frontend Setup

1. Open a new terminal.

2. Navigate to the frontend folder:

```bash
cd frontend
```

3. Install frontend dependencies:

```bash
npm install
```

4. Start the Vue development server:

```bash
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

# Automated Testing

The project includes automated backend API tests written using **pytest**.

The tests validate:

- API endpoint responses
- JSON response structure
- CRUD operations
- Error handling
- Performance checks

To run the automated tests:

```bash
pytest
```

Detailed testing instructions, configuration, and test file descriptions can be found here:

```
testing/automated/README.md
```

---

# Project Documentation

Additional documentation is available in the following locations:

| Document                | Location                                  |
|-------------------------|-------------------------------------------|
| QA Documentation        | testing/                                  |
| Automated Testing Guide | backend/automation_tests/README.md        |
| API Documentation       | API_DOCUMENTATION.md                      |
| Bug Reports             | testing/bug-reports/                      |
| Frontend Test Cases     | testing/frontend_test_files/test-cases.md |
| Backend Test Cases      | testing/backend_test_files/test-cases.md  |

---

# Manual QA Testing

Manual QA documentation is located in:

```
testing/
```

It contains:

- Frontend Test Plan
- Frontend Test Cases
- Backend Test Plan
- Backend Test Cases
- Smoke Testing
- API Testing
- UI Testing
- Bug Reports
- Regression Testing

---

# Testing Workflow

1. Smoke Testing
2. Functional Testing
3. API Testing
4. UI Testing
5. Bug Reporting
6. Regression Testing
7. Final QA Report

---

# Dependencies

Backend dependencies are managed through:

```
backend/requirements.txt
```

Frontend dependencies are managed through:

```
frontend/package.json
```

---

# Contributors

| Name              | Responsibility                                               |
|-------------------|--------------------------------------------------------------|
| Yagyha Abdul      | Team Leader                                                  |
| Maiesha Moohan    | Scrum Master                                                 |
| Nuriyah Davids    | Frontend QA | Frontend Testing, Documentation                |
| Angela Solomons   | Backend QA  | Backend Testing, Documentation                 |
| Elijah Lategan    | Dashboard & Debugging                                        |
| Butsha Tengwa     | Article Grid, Search bar functionality, Three.js & Debugging |
| Ishma-iel Gray    | Filter Functionality                                         |
| Zanda Kumsha      | Scrapers & Debugging                                         |
| Khanya Gcilitshane| Data Cleaning & Storage                                      |
| Karah Fisher      | APIs, Axios, Flask                                           |

---

# Documentation

Project documentation can be found in:

```
root/
```

- API Documentation
- README

```
testing/
```

- Test Plans
- Test Cases
- Bug Reports
- QA Reports
- Screenshots

---

# License

This project was developed for educational purposes as part of the Team Charlie Web Scraping Analytics Dashboard project.