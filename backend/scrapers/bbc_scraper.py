import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# Scrapes BBC RSS feed
def bbc_scraper():
    url = "https://feeds.bbci.co.uk/news/rss.xml"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        articles = []

        for item in items:
            article = {
                "title": item.title.text if item.title else "",
                "description": item.description.text if item.description else "",
                "link": item.link.text if item.link else "",
                "published": item.pubDate.text if item.pubDate else ""
            }
            articles.append(article)

        raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_file = raw_dir / "bbc_raw.json"

        with raw_file.open("w", encoding="utf-8") as file:
            json.dump(articles, file, indent=4, ensure_ascii=False)

        return {
            "success": True,
            "message": f"Successfully saved {len(articles)} articles as raw JSON.",
            "path": str(raw_file)
        }

    return {
        "success": False,
        "message": f"Failed to fetch RSS feed. Status code: {response.status_code}"
    }
    

        


