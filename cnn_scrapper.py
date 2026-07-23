#  # Scrapes CNN Html 

# from bs4 import BeautifulSoup
# import requests

# url = "https://edition.cnn.com/markets?utm_source=hp#econ-events"


# headers = {
#     "User-Agent": "Mozilla/5.0"
# }
# response = requests.get(url, headers=headers) 

# soup = BeautifulSoup(response.text, 'html.parser')

# with open("cnn.html", "w", encoding="utf-8") as f:
#     f.write(soup.prettify())

# classes = set()

# spans = soup.find_all(
#     "span",
#     class_="content-3ofLyd header-P1FM6v cnn-pcl-1ymzlgz"
# )

# print("Found:", len(spans))

# for span in spans:
#     print(span.get_text(strip=True))

# divs = soup.find_all(
#     "div",
#     class_="index-tabs-3jp4iL cnn-pcl-y6ghh0"
# )

# # for div in divs:
# #     print(div.get_text(strip=True))
# for div in divs:
#     print(div.get_text(strip=True), end="\t")


# divs = soup.find_all(
#     "div",
#     class_="cards-container-2w2La6 cnn-pcl-detjz"
# )


# for div in divs:
#     print(div.get_text(strip=True))

from bs4 import BeautifulSoup
import requests

# ============================================
# CNN Markets Page
# ============================================

url = "https://edition.cnn.com/markets"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Request failed! Status code: {response.status_code}")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Save HTML for inspection
with open("cnn.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("HTML saved as cnn.html\n")

# ============================================
# Find Header Spans
# ============================================

spans = soup.find_all(
    "span",
    class_="content-3ofLyd header-P1FM6v cnn-pcl-1ymzlgz"
)

print("=" * 60)
print("HEADER SPANS")
print("=" * 60)

if spans:
    for span in spans:
        print(span.get_text(strip=True))
else:
    print("No matching spans found.")

# ============================================
# Find Index Tabs
# ============================================

index_tabs = soup.find_all(
    "div",
    class_="index-tabs-3jp4iL cnn-pcl-y6ghh0"
)

print("\n" + "=" * 60)
print("INDEX TABS")
print("=" * 60)

if index_tabs:
    print(" | ".join(div.get_text(" ", strip=True) for div in index_tabs))
else:
    print("No matching index tabs found.")

# ============================================
# Find Cards Container
# ============================================

cards = soup.find_all(
    "div",
    class_="cards-container-2w2La6 cnn-pcl-detjz"
)

print("\n" + "=" * 60)
print("CARDS")
print("=" * 60)

if cards:
    print(" | ".join(div.get_text(" ", strip=True) for div in cards))
else:
    print("No matching cards found.")