import re
import json
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Common feed paths to try if the saved URL isn't a feed itself
FEED_GUESSES = ["", "/feed", "/feed/", "/rss", "/rss.xml", "/feed.xml", "/atom.xml"]


def _parse_feed(xml_content):
    """Parse RSS or Atom XML into a list of raw article dicts."""
    soup = BeautifulSoup(xml_content, "xml")
    items = soup.find_all("item") or soup.find_all("entry")  # RSS vs Atom
    articles = []

    for item in items:
        link_tag = item.find("link")
        link = ""
        if link_tag:
            link = link_tag.text.strip() or link_tag.get("href", "")

        articles.append({
            "title": item.title.text.strip() if item.title else "",
            "description": (
                item.description.text.strip() if item.description
                else (item.summary.text.strip() if item.summary else "")
            ),
            "link": link,
            "published": (
                item.pubDate.text.strip() if item.pubDate
                else (item.updated.text.strip() if item.updated else "")
            ),
        })
    return articles


def scrape_site(site):
    """
    Generic scraper for any site added via the Website Manager.
    Tries the saved URL as a feed, then a handful of common feed paths.
    Saves matched raw articles to data/raw/<slug>_raw.json, same shape
    as the hand-written scrapers, so clean_articles.py picks it up.
    """
    name = (site or {}).get("name", "Unknown")
    base_url = (site or {}).get("url", "").rstrip("/")
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "site"

    if not base_url:
        return {"success": False, "message": "No URL configured for this site."}

    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        return {"success": False, "message": f"'{base_url}' is not a valid URL."}

    tried = []
    for suffix in FEED_GUESSES:
        candidate = base_url + suffix if suffix else base_url
        tried.append(candidate)
        try:
            response = requests.get(
                candidate,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0 (TeamCharlieBot/1.0)"},
            )
        except requests.RequestException:
            continue

        if response.status_code != 200:
            continue

        try:
            articles = _parse_feed(response.content)
        except Exception:
            continue

        if articles:
            for article in articles:
                article["source"] = name

            raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_file = raw_dir / f"{slug}_raw.json"

            with raw_file.open("w", encoding="utf-8") as file:
                json.dump(articles, file, indent=4, ensure_ascii=False)

            return {
                "success": True,
                "message": f"Successfully saved {len(articles)} articles as raw JSON.",
                "path": str(raw_file),
            }

    return {
        "success": False,
        "message": f"Could not find a readable RSS/Atom feed for {name}. Tried: {', '.join(tried)}",
    }