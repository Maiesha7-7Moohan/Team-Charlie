import requests
import json
import os
from bs4 import BeautifulSoup

RSS_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    output_path = os.path.join(raw_dir, "coindesk_raw.json")

    try:
        response = requests.get(RSS_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": str(e)}

    rss = BeautifulSoup(response.content, "xml")
    items = rss.find_all("item")
    news_data = []

    for item in items:
        title = item.title.get_text(strip=True) if item.title else ""
        summary = item.description.get_text(strip=True) if item.description else ""
        article_url = item.link.get_text(strip=True) if item.link else ""
        published = item.pubDate.get_text(strip=True) if item.pubDate else ""
        author_tag = item.find("dc:creator")
        author = author_tag.get_text(strip=True) if author_tag else "Unknown"
        category_tag = item.find("category")
        category = category_tag.get_text(strip=True) if category_tag else "General"

        image = ""
        media = item.find("media:content")
        if media and media.get("url"):
            image = media["url"]

        article = ""
        if article_url:
            try:
                article_response = requests.get(article_url, headers=HEADERS, timeout=10)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, "html.parser")

                selectors = [
                    ("article", {}), ("main", {}),
                    ("div", {"data-testid": "article-content"}),
                    ("div", {"class": "article-content"}),
                    ("div", {"class": "content-body"}),
                    ("section", {"class": "article-body"}),
                ]
                article_container = None
                for tag, attrs in selectors:
                    article_container = article_soup.find(tag, attrs)
                    if article_container:
                        break

                paragraphs = (article_container or article_soup).find_all("p")
                seen = set()
                for p in paragraphs:
                    text = p.get_text(" ", strip=True)
                    if len(text) < 40 or text in seen:
                        continue
                    seen.add(text)
                    article += text + "\n\n"
                article = article.strip()
            except requests.exceptions.RequestException:
                pass

        news_data.append({
            "title": title, "summary": summary, "author": author,
            "category": category, "published": published, "source": "CoinDesk",
            "image_url": image, "article_url": article_url, "article": article,
        })

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(news_data, file, indent=4, ensure_ascii=False)

    return {"success": True, "articles_found": len(news_data), "path": output_path}


if __name__ == "__main__":
    print(run())