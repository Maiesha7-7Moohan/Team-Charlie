import requests
from bs4 import BeautifulSoup
import time

RSS_URL = "https://techcrunch.com/feed/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}


def scrape_article(url):
    """Scrape image and full article body."""

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Image
        image = ""
        image_meta = soup.find("meta", property="og:image")
        if image_meta:
            image = image_meta.get("content", "")

        # Summary (more accurate than RSS if available)
        summary = ""
        desc = soup.find("meta", attrs={"name": "description"})
        if desc:
            summary = desc.get("content", "")

        # Article body
        paragraphs = soup.find_all("p")

        article = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        return summary, image, article

    except Exception as e:
        print(f"Failed: {url}")
        print(e)
        return "", "", ""


def scrape_feed():

    response = requests.get(
        RSS_URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")

    articles = []

    for item in soup.find_all("item"):

        title = item.title.text if item.title else ""

        article_url = item.link.text if item.link else ""

        published = item.pubDate.text if item.pubDate else ""

        creator = item.find("dc:creator")
        author = creator.text if creator else ""

        categories = item.find_all("category")
        category = categories[0].text if categories else "Technology"

        print(f"Article: {title}")

        summary, image, article = scrape_article(article_url)

        articles.append({

            "title": title,

            "summary": summary,

            "author": author,

            "category": category,

            "published": published,

            "source": "TechCrunch",

            "image_url": image,

            "article_url": article_url,

            "article": article

        })

        time.sleep(1)

    return articles


def main():

    articles = scrape_feed()

    print(f"\nCollected {len(articles)} articles.\n")

    for article in articles:

        print("=" * 80)
        print("Title      :", article["title"])
        print("Summary    :", article["summary"])
        print("Author     :", article["author"])
        print("Category   :", article["category"])
        print("Published  :", article["published"])
        print("Source     :", article["source"])
        print("Image URL  :", article["image_url"])
        print("Article URL:", article["article_url"])
        print("Article Preview:")
        print(article["article"][:500])  # Show first 500 characters
        print()


if __name__ == "__main__":
    main()