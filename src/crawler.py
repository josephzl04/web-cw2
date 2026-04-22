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
    quote_blocks = soup.select(".quote")

    parts = []
    
    for quote in quote_blocks:
        text_element = quote.select_one(".text")
        author_element = quote.select_one(".author")
        tag_elements = quote.select(".tag")

        if text_element:
            parts.append(text_element.get_text(strip=True))

        if author_element:
            parts.append(author_element.get_text(strip=True))

        for tag in tag_elements:
            parts.append(tag.get_text(strip=True))

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

        html = fetch_page(url)
        if not html:
            print(f"Stopping crawl because page fetch failed: {url}")
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