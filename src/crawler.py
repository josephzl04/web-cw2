import time
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://quotes.toscrape.com/"

def fetch_page(url: str) -> str:
    """Fetches contents from target url"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


def extract_page_text(html: str) -> str:
    """Extract text content from HTML page"""
    soup = BeautifulSoup(html, 'html.parser')
    
    quotes = soup.select(".quote .text")
    authors = soup.select(".quote .author")
    tags = soup.select(".quote .tags")

    parts = []

    for i in range(len(quotes)):
        parts.append(quotes[i].get_text(strip=True))

        if i < len(authors):
            parts.append(authors[i].get_text(strip=True))

        if i < len(tags):
            parts.append(tags[i].get_text(" ", strip=True))

    return " ".join(parts)

def get_next_page_url(html: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.select_one("li.next a")

    if not next_link:
        return None
        
    href = next_link.get("href")
    if not href:
        return None

    return TARGET_URL.rstrip("/") + href

def crawl_quotes() -> list[dict]:
    url = TARGET_URL
    pages = []

    while url:
        print(f"Crawling {url}...")

        try:
            html = fetch_page(url)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            break

        text = extract_page_text(html)

        pages.append({
            "url": url,
            "text": text
        })

        next_url = get_next_page_url(html)

        if next_url:
            time.sleep(6)
            
        url = next_url
    return pages

if __name__ == "__main__":
    pages = crawl_quotes()
    print(f"\nCrawled {len(pages)} pages.\n")

    for page in pages[:2]:
        print(page["url"])
        print(page["text"][:300])
        print()