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