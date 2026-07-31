import json
import os
from datetime import datetime


# ============================================
# Clean Text
# ============================================

def clean_text(text):
    """Remove unnecessary spaces and new lines."""

    if not text:
        return ""

    return " ".join(
        str(text).split()
    ).strip()


# ============================================
# Clean Dates
# ============================================

def clean_date(date_text):
    """Convert different date formats into one standard format."""

    if not date_text:
        return None

    date_text = str(
        date_text
    ).strip()

    date_formats = [

        "%a, %d %b %Y %H:%M:%S GMT",

        "%a, %d %b %Y %H:%M:%S %z",

        "%Y-%m-%dT%H:%M:%S%z",

        "%Y-%m-%dT%H:%M:%S.%f%z",

        "%Y-%m-%d %H:%M:%S"

    ]

    for date_format in date_formats:

        try:

            date_object = datetime.strptime(

                date_text,

                date_format

            )

            return date_object.strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        except ValueError:

            continue

    return None


# ============================================
# Get Category
# ============================================

def get_category(article):
    """Get the article category."""

    category = article.get(
        "category",
        ""
    )

    if category:

        return clean_text(
            category
        )

    link = (

        article.get(
            "link",
            ""
        )

        or article.get(
            "article_url",
            ""
        )

    )

    link = link.lower()


    if "/sport/" in link:

        return "Sport"


    if "/weather/" in link:

        return "Weather"


    if "/sounds/" in link:

        return "Podcast"


    if "/iplayer/" in link:

        return "Video"


    return "News"


# ============================================
# Get Source
# ============================================

def get_source(article, link):
    """Get the news source."""

    source = clean_text(

        article.get(
            "source",
            ""
        )

    )


    if source:

        return source


    link = link.lower()


    if "bbc.co.uk" in link:

        return "BBC"


    if "bbc.com" in link:

        return "BBC"


    if "cnn.com" in link:

        return "CNN"


    if "techcrunch.com" in link:

        return "TechCrunch"


    if "coindesk.com" in link:

        return "CoinDesk"


    return "Unknown"


# ============================================
# Clean One Article
# ============================================

def clean_article(article):
    """Clean and standardize one article."""

    title = clean_text(

        article.get(
            "title",
            ""
        )

    )


    description = clean_text(

        article.get(
            "description",
            ""

        )

        or article.get(
            "summary",
            ""
        )

    )


    link = (

        article.get(
            "link",
            ""
        )

        or article.get(
            "article_url",
            ""
        )

    ).strip()


    published = clean_date(

        article.get(
            "published",
            ""
        )

    )


    author = clean_text(

        article.get(
            "author",
            ""
        )

    )


    category = get_category(
        article
    )


    source = get_source(

        article,

        link

    )


    image_url = (

        article.get(
            "image_url",
            ""
        )

    ).strip()


    article_body = clean_text(

        article.get(
            "article",
            ""
        )

    )


    return {

        "title": title,

        "description": description,

        "link": link,

        "published": published,

        "author": author,

        "category": category,

        "source": source,

        "image_url": image_url,

        "article": article_body

    }


# ============================================
# Load JSON File
# ============================================

def load_json(file_path):
    """Load a JSON file if it exists."""

    if not os.path.exists(
        file_path
    ):

        print(
            f"File not found: {file_path}"
        )

        return []


    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(
            file
        )


# ============================================
# Load Raw Data
# ============================================

bbc_articles = load_json(

    "data/raw/bbc_raw.json"

)


cnn_articles = load_json(

    "data/raw/cnn_raw.json"

)


techcrunch_articles = load_json(

    "data/raw/techcrunch_raw.json"

)


coindesk_articles = load_json(

    "data/raw/coindesk_raw.json"

)


# ============================================
# Combine All Articles
# ============================================

all_articles = (

    bbc_articles

    + cnn_articles

    + techcrunch_articles

    + coindesk_articles

)


# ============================================
# Clean Articles
# ============================================

cleaned_articles = []

seen_links = set()


for article in all_articles:

    cleaned_article = clean_article(
        article
    )


    title = cleaned_article[
        "title"
    ]


    link = cleaned_article[
        "link"
    ]


    # Skip articles without a title
    if not title:

        continue


    # Skip articles without a link
    if not link:

        continue


    # Skip duplicate articles
    if link in seen_links:

        continue


    seen_links.add(
        link
    )


    cleaned_articles.append(
        cleaned_article
    )


# ============================================
# Create Cleaned Folder
# ============================================

os.makedirs(

    "data/cleaned",

    exist_ok=True

)


# ============================================
# Save Cleaned Data
# ============================================

output_file = (

    "data/cleaned/"
    "articles_cleaned.json"

)


with open(

    output_file,

    "w",

    encoding="utf-8"

) as file:

    json.dump(

        cleaned_articles,

        file,

        indent=4,

        ensure_ascii=False

    )


# ============================================
# Completion Message
# ============================================

print(

    f"Successfully cleaned and saved "

    f"{len(cleaned_articles)} articles."

)


print(

    f"Output file: {output_file}"

)