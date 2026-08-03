# Team-Charlie
# Data Cleaning, Organization, and Storage

## Overview

This part of the project is responsible for transforming the raw news articles collected by the web scrapers into a clean, consistent, and organized format that can be used by the backend API and frontend application.

My role in the project was to design and implement the data processing workflow by cleaning the scraped data, organizing it into a consistent structure, and storing it in the appropriate project directories.

---

## Responsibilities

* Clean raw scraped news data.
* Remove duplicate or unnecessary information.
* Standardize article fields across different news sources.
* Organize data into a clear folder structure.
* Store processed data in JSON format for easy access by the application.

---

## Folder Structure

```text
backend/
│
├── cleaning/
│   └── (data cleaning scripts)
│
├── data/
│   ├── raw/
│   │   ├── bbc_raw.json
│   │   ├── cnn_raw.json
│   │   ├── coindesk_raw.json
│   │   └── techcrunch_raw.json
│   │
│   └── cleaned/
│       └── (processed JSON files)
│
└── scrapers/
    ├── bbc_scraper.py
    ├── cnn_scraper.py
    ├── coindesk_scraper.py
    └── techcrunch_scraper.py
```

---

## Data Processing Workflow

1. News articles are scraped from multiple news websites.
2. The raw data is saved in the `backend/data/raw/` directory.
3. Cleaning scripts process the raw files by:

   * Removing duplicate articles.
   * Removing unnecessary whitespace.
   * Standardizing field names.
   * Handling missing values where possible.
4. The cleaned data is stored in a structured JSON format for use by the application.

---

## Data Format

Each cleaned article follows a consistent structure similar to:

```json
{
  "title": "Article Title",
  "author": "Author Name",
  "published": "2026-07-31",
  "summary": "Short summary of the article.",
  "url": "https://example.com/article",
  "image": "https://example.com/image.jpg",
  "source": "BBC"
}
```

---

## Technologies Used

* Python
* JSON
* Requests
* BeautifulSoup
* File handling (`json` module)

---

## Outcome

The cleaning and organization process ensures that data from different news sources is stored in a consistent format, making it easier for the backend to serve the data and for the frontend to display articles reliably.

This workflow also improves data quality by reducing duplicates, standardizing fields, and maintaining an organized project structure for future development.

Author: Khanya Gcilitshaneg
Role: Data Cleaning, Organization, and Storage
