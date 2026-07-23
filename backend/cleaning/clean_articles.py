import json
import os
from datetime import datetime

def clean_text(text):
    """Remove unnecessary spaces and new lines."""

    if not text:
        return""

    return " ".join(text.split()).strip()

def clean_date(date_text):
    """Convert BBC date into a standard format."""

    if not date_text:
        return None

    try:
        date_object = datetime.strptime(
            date_text,
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        return date_object.strftime(
           "%Y-%m-%d %H:%M:%S" 
        )

    except ValueError:
        return None

def get_category(link):
    """Determine the category from thr BBC link."""

    if "/sport/" in link:
        return "Sport"

    if "/weather/" in link:
        return "Weather"

    if "/sounds/" in link:
        return "Podcast"

    if "/iplayer/" in link:
        return "Video"

    return "News"

# Load raw data
with open(
    "data/raw/bbc_raw.json",
    "r",
    encoding="utf-8"
) as file:

    raw_articles = json.load(file)

cleaned_articles = []
seen_links = set()

for article in raw_articles:

    title = clean_text(
        article.get("title", "")
    )

    description = clean_text(
        article.get("description", "")
    )

    link = article.get(
        "link",
        ""
    ).strip()

    published = clean_date(
        article.get(
            "published",
            ""
        )
    )

    # Skip articles without a title or link
    if not title or not link:
        continue

    # Skip duplicate articles
    if link in seen_links:
        continue

    seen_links.add(link)

    cleaned_article = {
        "title": title,
        "description": description,
        "link": link,
        "published": published,
        "source": "BBC",
        "category": get_category(link)
    }

    cleaned_articles.append(
        cleaned_article
    )

# Create cleaned folder
os.makedirs(
    "data/cleaned",
    exist_ok=True
)

# Save cleaned folder
with open(
    "data/cleaned/bbc_cleaned.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        cleaned_articles,
        file,
        indent=4,
        ensure_ascii=False
    )

print(
    f"Successfully cleaned and saved"
    f" {len(cleaned_articles)} articles."
)