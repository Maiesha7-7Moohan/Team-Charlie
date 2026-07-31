# 09 - Scraper Testing

## Purpose

Verify that the individual news scrapers implemented in the `feature/parsing` branch can successfully retrieve and parse article data from their assigned news sources.

## Testing Scope

This testing covers scraper functionality only.

Included:
- BBC RSS scraper
- CNN scraper
- CoinDesk scraper
- TechCrunch scraper

Excluded:
- Data cleaning pipeline
- JSON storage validation
- API testing
- Frontend/dashboard testing
- Full system integration testing

These areas will be tested when the relevant branches and components are available.

---

# TC-SCRAPER-001: BBC RSS Scraper

## Test Type

Functional Testing

## Feature

BBC News RSS Scraping

## Objective

Verify that the BBC RSS scraper can retrieve and extract article information from the BBC RSS feed.

## Preconditions

- Python installed
- Internet connection available
- Required dependencies installed:
  - requests
  - beautifulsoup4
  - lxml

## Test Steps

| Step | Action |
|---|---|
| 1 | Navigate to feature/parsing - Backend folder |
| 2 | Run `python scrapers/bbc_scrapper.py` |
| 3 | Observe the terminal output |

## Expected Result

The scraper successfully retrieves BBC articles and extracts:

- Article title
- Article description
- Article link
- Publication date

## Actual Result

The scraper successfully retrieved multiple BBC articles and displayed the required article information.

The following fields were successfully extracted:

- Title
- Description
- Link
- Published date

## Status

PASS

## Notes

Initial execution failed because the XML parser dependency required by BeautifulSoup was missing.

Error encountered:

```text
bs4.exceptions.FeatureNotFound: Couldn't find a tree builder with the features you requested: xml. Do you need to install a parser library?






<!-- NEW -->

# 09 - Scraper Testing

## Purpose

Verify that the individual news scrapers implemented in the `feature/parsing` branch can successfully retrieve and parse article data from their assigned news sources.

## Testing Scope

This testing covers scraper functionality only.

Included:
- BBC RSS scraper
- CNN scraper
- CoinDesk scraper
- TechCrunch scraper

Excluded:
- Data cleaning pipeline
- JSON storage validation
- API testing
- Frontend/dashboard testing
- Full system integration testing

These areas will be tested when the relevant branches and components are available.

---

# TC-SCRAPER-001: BBC RSS Scraper

## Test Type

Functional Testing

## Feature

BBC News RSS Scraping

## Objective

Verify that the BBC RSS scraper can retrieve and extract article information from the BBC RSS feed cleanly and defensively without runtime exceptions.

## Preconditions

- Python installed
- Internet connection available
- Required dependencies installed manually:
  - `requests`
  - `beautifulsoup4`
  - `lxml`

## Test Steps

| Step | Action |
|---|---|
| 1 | Navigate to feature/parsing - Backend folder |
| 2 | Run `python scrapers/bbc_scrapper.py` (or `bbc_rss_scraper.py`) |
| 3 | Observe the terminal output |

## Expected Result

The scraper successfully retrieves BBC articles and extracts:

- Article title
- Article description
- Article link
- Publication date

## Actual Result

**July 28, 2026:**  
The scraper failed during initial setup because there was no `requirements.txt` file present in the repository to define project dependencies. As a result, the required `lxml` XML parser dependency for BeautifulSoup was missing on the environment.

**July 29, 2026 (Retest):**  
Dependencies were manually installed and verified. Re-tested the scraper on `feature/parsing`. The script executed cleanly without raising `AttributeError` exceptions when handling missing XML tags, successfully extracting:
- Title
- Description
- Link
- Published date

## Status

PASS

## Execution Log

| Date | Tester | Result | Comments |
|---|---|---|---|
| July 28, 2026 | Angela Solomons | FAIL | Failed on setup: No `requirements.txt` file provided; missing `lxml` XML parser library. |
| July 29, 2026 | Angela Solomons | PASS | Manually installed `lxml`, verified defensive parsing logic, and signed off on `feature/parsing`. |

## Notes

**July 28, 2026:**  
Initial execution failed because no `requirements.txt` file existed in the branch to manage environment setup, leading to a missing XML parser dependency (`lxml`) required by BeautifulSoup.

Error encountered:

```text
bs4.exceptions.FeatureNotFound: Couldn't find a tree builder with the features you requested: xml. Do you need to install a parser library?