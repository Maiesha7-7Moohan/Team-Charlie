from bs4 import BeautifulSoup
import requests

url = "https://feeds.bbci.co.uk/news/rss.xml"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "xml")

    items = soup.find_all("item")

    for item in items:
        title = item.title.text
        description = item.description.text
        link = item.link.text
        pub_date = item.pubDate.text

        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Link: {link}")
        print(f"Published: {pub_date}")
        print("-" * 50)
else:
    print(f"Failed to fetch RSS feed. Status code: {response.status_code}")