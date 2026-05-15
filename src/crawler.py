import time
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://quotes.toscrape.com/"
TARGET_DOMAIN = urlparse(TARGET_URL).netloc


def fetch_page(url):
    """Fetches contents from target url"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_page_text(html):
    """Extract text content from HTML page"""
    soup = BeautifulSoup(html, "html.parser")
    quote_blocks = soup.select(".quote")

    parts = []

    if quote_blocks:
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

    for unwanted in soup(["script", "style"]):
        unwanted.decompose()

    return soup.get_text(" ", strip=True)

def normalise_internal_url(current_url, href):
    """
    Convert a link into a full internal URL, or return None for external links.
    """
    if not href:
        return None

    absolute_url = urljoin(current_url, href)
    absolute_url, _ = urldefrag(absolute_url)

    parsed_url = urlparse(absolute_url)

    if parsed_url.scheme not in ("http", "https"):
        return None

    if parsed_url.netloc != TARGET_DOMAIN:
        return None

    return absolute_url


def get_internal_links(html, current_url):
    """
    Return all internal links found on the current page.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for link in soup.select("a[href]"):
        internal_url = normalise_internal_url(current_url, link.get("href"))

        if internal_url:
            links.add(internal_url)

    return sorted(links)


def crawl_quotes():
    """
    Crawl all reachable internal pages and return a list of page dictionaries.
    """
    pages = []
    visited = set()
    to_visit = [TARGET_URL]

    while to_visit:
        url = to_visit.pop(0)

        if url in visited:
            continue

        if visited:
            time.sleep(6)

        print(f"Crawling {url}...")

        visited.add(url)
        html = fetch_page(url)

        if not html:
            print(f"Skipping page because page fetch failed: {url}")
            continue

        text = extract_page_text(html)

        pages.append({
            "url": url,
            "text": text
        })

        for link in get_internal_links(html, url):
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    return pages


if __name__ == "__main__":
    pages = crawl_quotes()
    print(f"\nCrawled {len(pages)} pages.\n")

    for page in pages[:2]:
        print(page["url"])
        print(page["text"][:300])
        print()