import requests
import json
from bs4 import BeautifulSoup


# ============================================
# Configuration
# ============================================

RSS_URL = (
    "https://www.coindesk.com/"
    "arc/outboundfeeds/rss/"
    "?outputType=xml"
)

OUTPUT_FILE = (
    "data/raw/coindesk_raw.json"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


# ============================================
# Download RSS Feed
# ============================================

try:

    response = requests.get(
        RSS_URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

except requests.exceptions.RequestException as e:

    print(
        f"Failed to fetch RSS feed:\n{e}"
    )

    exit()


# ============================================
# Parse RSS Feed
# ============================================

rss = BeautifulSoup(
    response.content,
    "xml"
)

items = rss.find_all(
    "item"
)

print(
    f"Found {len(items)} articles.\n"
)


news_data = []


# ============================================
# Scrape Each Article
# ============================================

for item in items:

    title = (

        item.title.get_text(
            strip=True
        )

        if item.title

        else ""

    )


    summary = (

        item.description.get_text(
            strip=True
        )

        if item.description

        else ""

    )


    article_url = (

        item.link.get_text(
            strip=True
        )

        if item.link

        else ""

    )


    published = (

        item.pubDate.get_text(
            strip=True
        )

        if item.pubDate

        else ""

    )


    author_tag = item.find(
        "dc:creator"
    )


    author = (

        author_tag.get_text(
            strip=True
        )

        if author_tag

        else ""

    )


    category_tag = item.find(
        "category"
    )


    category = (

        category_tag.get_text(
            strip=True
        )

        if category_tag

        else "General"

    )


    image = ""


    media = item.find(
        "media:content"
    )


    if media and media.get("url"):

        image = media.get(
            "url"
        )


    article = ""


    # ========================================
    # Visit Article Page
    # ========================================

    if article_url:

        print(
            f"Article: {title}"
        )


        try:

            article_response = requests.get(

                article_url,

                headers=HEADERS,

                timeout=20

            )


            article_response.raise_for_status()


            article_soup = BeautifulSoup(

                article_response.text,

                "html.parser"

            )


            selectors = [

                (
                    "article",
                    {}
                ),

                (
                    "main",
                    {}
                ),

                (
                    "div",
                    {
                        "data-testid":
                        "article-content"
                    }
                ),

                (
                    "div",
                    {
                        "class":
                        "article-content"
                    }
                ),

                (
                    "div",
                    {
                        "class":
                        "content-body"
                    }
                ),

                (
                    "section",
                    {
                        "class":
                        "article-body"
                    }
                )

            ]


            article_container = None


            for tag, attrs in selectors:

                article_container = (
                    article_soup.find(
                        tag,
                        attrs
                    )
                )


                if article_container:

                    break


            if article_container:

                paragraphs = (

                    article_container.find_all(
                        "p"
                    )

                )

            else:

                paragraphs = (

                    article_soup.find_all(
                        "p"
                    )

                )


            seen = set()

            paragraphs_text = []


            for paragraph in paragraphs:

                text = paragraph.get_text(
                    " ",
                    strip=True
                )


                if len(text) < 40:

                    continue


                if text in seen:

                    continue


                seen.add(
                    text
                )


                paragraphs_text.append(
                    text
                )


            article = "\n\n".join(
                paragraphs_text
            )


        except requests.exceptions.RequestException as e:

            print(
                f"Failed to scrape article:"
                f"\n{article_url}"
            )

            print(e)


    # ========================================
    # Store Data
    # ========================================

    news_data.append({

        "title": title,

        "summary": summary,

        "author": author,

        "category": category,

        "published": published,

        "source": "CoinDesk",

        "image_url": image,

        "article_url": article_url,

        "article": article

    })


# ============================================
# Save Raw JSON
# ============================================

with open(

    OUTPUT_FILE,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        news_data,

        file,

        indent=4,

        ensure_ascii=False

    )


print(

    f"\nSaved {len(news_data)} articles to "

    f"'{OUTPUT_FILE}'."

)