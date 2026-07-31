from bs4 import BeautifulSoup
import requests
import json

 # Scrapes BBC RSS
 # feed for bbc
url = "https://feeds.bbci.co.uk/news/rss.xml"

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.content,"xml")

    items = soup.find_all("item")

    articles = []

    for item in items:
        article ={
            "title": item.title.text,
            "description": item.description.text,
            "link": item.link.text,
            "published": item.pubDate.text
        }

        articles.append(article)

    with open(
        "data/raw/bbc_raw.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            articles,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Successfully saved {len(articles)} articles"
        "as raw JSON."
    )


else:

    print(
        f"Failed to fecth RSS feed. "
        f"Status code: {response.status_code}"
    )

        


