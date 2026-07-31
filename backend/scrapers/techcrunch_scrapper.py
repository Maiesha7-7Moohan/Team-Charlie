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
    """Scrape additional details from the article page."""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Image
        image = ""

        meta = soup.find(
            "meta",
            property="og:image"
        )

        if meta:
            image = meta.get("content", "")

        # Article Body
        paragraphs = soup.find_all("p")

        article = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        return image, article

    except Exception as e:
        print(f"Failed to scrape {url}")
        print(e)
        return "", ""


def scrape_feed():

    response = requests.get(
        RSS_URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.content,
        "xml"
    )

    articles = []

    for item in soup.find_all("item"):

        title = item.title.text if item.title else ""

        summary = item.description.text if item.description else ""

        article_url = item.link.text if item.link else ""

        published = item.pubDate.text if item.pubDate else ""

        creator = item.find("dc:creator")
        author = creator.text if creator else ""

        categories = item.find_all("category")

        category = (
            categories[0].text
            if categories
            else "Technology"
        )

        print(f"Article: {title}")

        image, article = scrape_article(article_url)

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

    print(f"\nCollected {len(articles)} articles.")

    # Preview the first few articles
    for article in articles[:5]:
        print("-" * 60)
        print("Title:", article["title"])
        print("Author:", article["author"])
        print("Category:", article["category"])
        print("Published:", article["published"])
        print("URL:", article["article_url"])


if __name__ == "__main__":
    main()