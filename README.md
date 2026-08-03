# Team-Charlie

# 📰 Multi-Source News Scraper - Code Explanation

## Overview

This project consists of multiple Python web scrapers that collect news articles from different news providers. Each scraper is written specifically for the structure of its target website because every news source stores its content differently.

The project uses the following Python libraries:

- `requests` – Sends HTTP requests to websites.
- `BeautifulSoup` – Parses HTML and XML documents.
- `json` – Stores scraped articles in JSON format.
- `urllib.parse` – Processes and validates URLs.
- `time` – Adds delays between requests to avoid overwhelming servers.

---

# Project Structure

```text
backend/
│
├── scrapers/
│   ├── __init__.py
│   ├── bbc_scrapper.py
│   ├── cnn_scrapper.py
│   ├── coindesk_scraper.py
│   ├── techcrunch_scrapper.py
│
├── data/
│   ├── cnn_news.json
│   ├── coindesk_articles.json
│
└── README.md
```

---

# `__init__.py`

This file marks the `scrapers` directory as a Python package.

```python
# Python package
```

It does not contain any executable code, but it allows Python to import modules from the folder correctly.

---

# BBC Scraper (`bbc_scrapper.py`)

## Purpose

The BBC scraper reads the BBC News RSS feed and extracts article information directly from XML.

---

## Step 1 – Import Libraries

```python
from bs4 import BeautifulSoup
import requests
```

- `requests` downloads the RSS feed.
- `BeautifulSoup` parses the XML response.

---

## Step 2 – Define the RSS Feed

```python
url = "https://feeds.bbci.co.uk/news/rss.xml"
```

The BBC provides an RSS feed containing recent news articles. Instead of scraping HTML pages, the program reads this structured XML feed.

---

## Step 3 – Download the Feed

```python
response = requests.get(url)
```

An HTTP GET request is sent to the RSS feed.

---

## Step 4 – Check the Response

```python
if response.status_code == 200:
```

The program only continues if the request was successful.

---

## Step 5 – Parse XML

```python
soup = BeautifulSoup(response.content, "xml")
```

The XML document is loaded into BeautifulSoup.

---

## Step 6 – Find Articles

```python
items = soup.find_all("item")
```

Each `<item>` represents one news article.

---

## Step 7 – Extract Information

For every article the scraper collects:

- Title
- Description
- Link
- Publication Date

The values are printed to the terminal.

---

# CNN Scraper (`cnn_scrapper.py`)

Unlike BBC, CNN does not provide the required information through a simple RSS feed.

Instead, the scraper crawls the CNN website.

---

## Configuration

Several constants are declared at the beginning.

### BASE_URL

```python
BASE_URL = "https://edition.cnn.com/"
```

This is the starting page.

### HEADERS

A browser User-Agent is added.

```python
HEADERS = {
    "User-Agent": "Mozilla..."
}
```

Some websites block requests that do not appear to come from a web browser.

---

## SKIP_PATHS

```python
SKIP_PATHS = [
    "/videos/",
    "/search",
    "/gallery/",
    ...
]
```

These paths are ignored because they are not article pages.

---

## KNOWN_CATEGORIES

```python
KNOWN_CATEGORIES = {
    "business",
    "politics",
    "health",
    ...
}
```

The scraper uses URL paths to determine the article category.

---

## Function: `get_article_links()`

This function:

1. Downloads the CNN homepage.
2. Parses the HTML.
3. Finds every hyperlink.
4. Converts relative URLs into absolute URLs.
5. Removes duplicates.
6. Filters unwanted links.
7. Returns valid article URLs.

```python
links = set()
```

A **set** is used because it automatically removes duplicate URLs.

---

## Function: `extract_category(url)`

The URL is split into parts.

Example:

```
https://edition.cnn.com/politics/article-name
```

becomes

```
politics
```

If no known category exists, the function returns:

```
General
```

---

## Function: `extract_article(url)`

This is the largest function in the project.

It visits every article page individually.

The function extracts:

- Title
- Summary
- Author
- Publication date
- Featured image
- Article body

Different HTML selectors are attempted because CNN pages are not always identical.

If one selector fails, the next selector is tried.

This makes the scraper much more reliable when page layouts change.

---

## JSON Output

After collecting all information, every article is saved as a Python dictionary.

Example:

```python
{
    "title": "...",
    "summary": "...",
    "author": "...",
    "category": "...",
    "published": "...",
    "source": "CNN",
    "image_url": "...",
    "article_url": "...",
    "article": "..."
}
```

The dictionaries are written to **cnn_news.json**, producing a structured dataset.

---

# CoinDesk Scraper (`coindesk_scraper.py`)

The CoinDesk scraper combines RSS parsing with full webpage scraping.

---

## Configuration

```python
RSS_URL
HEADERS
OUTPUT_FILE
```

These values define:

- where articles come from,
- how requests are sent,
- where data will be stored.

---

## Download RSS Feed

The scraper downloads the RSS feed using:

```python
requests.get()
```

Error handling is included:

```python
try:
    ...
except RequestException:
```

This prevents crashes if the network fails.

---

## Parse XML

BeautifulSoup reads the XML feed.

```python
rss = BeautifulSoup(response.content, "xml")
```

Then:

```python
items = rss.find_all("item")
```

retrieves every article.

---

## Scrape Individual Articles

For each article, the scraper extracts metadata from the RSS feed before opening the article page itself.

It then searches for several possible article containers:

```python
article
main
div
section
```

If none exist, it falls back to all paragraph elements.

---

## Removing Duplicate Paragraphs

```python
seen = set()
```

Every paragraph is checked before being added.

Duplicate paragraphs are skipped.

This produces much cleaner article text.

---

# TechCrunch Scraper (`techcrunch_scrapper.py`)

TechCrunch also uses an RSS feed.

---

## Function: `scrape_article(url)`

This function opens an individual article page.

It extracts:

- Featured image
- Every paragraph
- Complete article body

The article paragraphs are joined together using:

```python
"\n".join(...)
```

to produce readable text.

---

## Function: `scrape_feed()`

This function:

1. Downloads the RSS feed.
2. Reads every item.
3. Extracts metadata.
4. Calls `scrape_article()`.
5. Builds a dictionary.
6. Appends it to a list.

A one-second delay is included:

```python
time.sleep(1)
```

to reduce request frequency.

---

## Function: `main()`

The `main()` function controls the execution flow.

It:

1. Calls `scrape_feed()`.
2. Stores the returned articles.
3. Prints a preview of the first five articles.

The script only runs when executed directly because of:

```python
if __name__ == "__main__":
```

This prevents the scraper from running automatically if it is imported into another Python module.

---

# JSON Files

The project stores scraped data in JSON format.

Each article contains the same structure regardless of the source.

Fields include:

- title
- summary
- author
- category
- published
- source
- image_url
- article_url
- article

Using a consistent schema allows articles from multiple news providers to be combined into a single dataset.

---

# Programming Concepts Demonstrated

This project demonstrates several important Python concepts:

- Functions
- Modular programming
- HTTP requests
- XML parsing
- HTML parsing
- Web scraping
- JSON serialization
- Error handling with `try/except`
- Loops
- Conditional statements
- Lists
- Sets
- Dictionaries
- URL parsing
- File handling

---

# Execution Flow

The overall execution process is:

1. Connect to a news source.
2. Download the RSS feed or homepage.
3. Parse the response using BeautifulSoup.
4. Locate article links.
5. Visit each article page.
6. Extract metadata.
7. Extract the article body.
8. Build a Python dictionary.
9. Append the dictionary to a list.

This modular design makes it easy to add new news providers in the future by creating another scraper that follows the same workflow.

---
