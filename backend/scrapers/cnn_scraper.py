import json
import time
import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


BASE_URL = "https://edition.cnn.com/"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}


SKIP_PATHS = [
    "/videos/",
    "/video/",
    "/audio/",
    "/search",
    "/weather",
    "/live-news/",
    "/interactive/",
    "/photos/",
    "/gallery/",
    "/markets",
    "/profile",
    "#"
]


KNOWN_CATEGORIES = {
    "business",
    "world",
    "politics",
    "health",
    "sport",
    "sports",
    "travel",
    "style",
    "science",
    "tech",
    "technology",
    "entertainment",
    "us"
}


def get_article_links():

    print("Loading CNN homepage...")

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = set()

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"].strip()

        if href.startswith("/"):

            href = urljoin(
                BASE_URL,
                href
            )

        if not href.startswith(
            "https://edition.cnn.com"
        ):

            continue

        if any(
            skip in href
            for skip in SKIP_PATHS
        ):

            continue

        links.add(
            href
        )

    return sorted(
        links
    )


def extract_category(url):

    parts = [

        part.lower()

        for part in urlparse(
            url
        ).path.split("/")

        if part

    ]

    for part in parts:

        if part in KNOWN_CATEGORIES:

            return part.capitalize()

    return "General"


def extract_article(url):

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=20

        )

        if response.status_code != 200:

            return None

        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )

        # Title
        title = ""

        meta = soup.find(

            "meta",

            property="og:title"

        )

        if meta:

            title = meta.get(

                "content",

                ""

            )

        if not title:

            h1 = soup.find(
                "h1"
            )

            if h1:

                title = h1.get_text(
                    strip=True
                )

        if not title:

            return None

        # Summary
        summary = ""

        meta = soup.find(

            "meta",

            attrs={
                "name": "description"
            }

        )

        if meta:

            summary = meta.get(

                "content",

                ""

            )

        # Author
        author = ""

        selectors = [

            (
                "meta",
                {
                    "name": "author"
                }
            ),

            (
                "meta",
                {
                    "property": "author"
                }
            ),

            (
                "meta",
                {
                    "name": "parsely-author"
                }
            )

        ]

        for tag, attrs in selectors:

            meta = soup.find(

                tag,

                attrs=attrs

            )

            if meta:

                author = meta.get(

                    "content",

                    ""

                )

                break

        # Published date
        published = ""

        meta = soup.find(

            "meta",

            property="article:published_time"

        )

        if meta:

            published = meta.get(

                "content",

                ""

            )

        # Image
        image = ""

        meta = soup.find(

            "meta",

            property="og:image"

        )

        if meta:

            image = meta.get(

                "content",

                ""

            )

        # Article body
        article_tag = soup.find(
            "article"
        )

        if article_tag:

            paragraphs = article_tag.find_all(
                "p"
            )

        else:

            paragraphs = soup.find_all(
                "p"
            )

        body = "\n".join(

            p.get_text(
                " ",
                strip=True
            )

            for p in paragraphs

        )

        return {

            "title": title,

            "summary": summary,

            "author": author,

            "category": extract_category(
                url
            ),

            "published": published,

            "source": "CNN",

            "image_url": image,

            "article_url": url,

            "article": body

        }

    except Exception as e:

        print(
            f"Failed: {url}"
        )

        print(
            e
        )

        return None


def main():

    links = get_article_links()

    print(
        f"\nFound {len(links)} links.\n"
    )

    articles = {}

    for i, link in enumerate(

        links,

        start=1

    ):

        print(

            f"[{i}/{len(links)}] {link}"

        )

        article = extract_article(

            link

        )

        if article:

            articles[
                article["article_url"]
            ] = article

            print(

                f"✓ {article['title']}"

            )

        time.sleep(
            1
        )

    data = list(
        articles.values()
    )

    # Create data/raw folder if it does not exist
    os.makedirs(

        "data/raw",

        exist_ok=True

    )

    # Save raw CNN data
    with open(

        "data/raw/cnn_raw.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    print(

        f"\nSaved {len(data)} articles."

    )

    print(

        "Output: data/raw/cnn_raw.json"

    )


if __name__ == "__main__":

    main()