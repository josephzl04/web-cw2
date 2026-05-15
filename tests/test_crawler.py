import requests
from src.crawler import TARGET_URL, crawl_quotes, fetch_page, get_internal_links, extract_page_text

def test_extract_page_text():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">"A test quote"</span>
                <span class="author">Test author</span>
                <div class="tags">
                    <a class="tag">Test tag 1</a>
                    <a class="tag">Test tag 2</a>
                </div>
            </div>
        </body>
    </html>
    """
    text = extract_page_text(html)
    assert "A test quote" in text
    assert "Test author" in text
    assert "Test tag 1" in text
    assert "Test tag 2" in text

def test_fetch_page_returns_empty_string_on_request_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Network error")

    monkeypatch.setattr("src.crawler.requests.get", mock_get)

    assert fetch_page("https://quotes.toscrape.com/") == ""

def test_crawl_quotes_respects_politeness_window(monkeypatch):
    first_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">"First quote"</span>
                <span class="author">First author</span>
                <a class="tag">First tag</a>
            </div>
            <li class="next">
                <a href="/page/2/">Next</a>
            </li>
        </body>
    </html>
    """

    second_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">"Second quote"</span>
                <span class="author">Second author</span>
                <a class="tag">Second tag</a>
            </div>
        </body>
    </html>
    """

    html_by_url = {
        TARGET_URL: first_html,
        "https://quotes.toscrape.com/page/2/": second_html
    }

    sleep_calls = []

    monkeypatch.setattr("src.crawler.fetch_page", lambda url: html_by_url.get(url, ""))
    monkeypatch.setattr("src.crawler.time.sleep", lambda seconds: sleep_calls.append(seconds))

    pages = crawl_quotes()

    assert len(pages) == 2
    assert "First quote" in pages[0]["text"]
    assert "Second quote" in pages[1]["text"]
    assert pages[0]["url"] == TARGET_URL
    assert pages[1]["url"] == "https://quotes.toscrape.com/page/2/"
    assert sleep_calls == [6]

def test_crawl_quotes_stops_on_fetch_error(monkeypatch):
    first_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">"First quote"</span>
                <span class="author">First author</span>
                <a class="tag">First tag</a>
            </div>
            <li class="next">
                <a href="/page/2/">Next</a>
            </li>
        </body>
    </html>
    """

    html_by_url = {
        TARGET_URL: first_html,
        "https://quotes.toscrape.com/page/2/": ""
    }

    sleep_calls = []

    monkeypatch.setattr("src.crawler.fetch_page", lambda url: html_by_url.get(url, ""))
    monkeypatch.setattr("src.crawler.time.sleep", lambda seconds: sleep_calls.append(seconds))

    pages = crawl_quotes()

    assert len(pages) == 1
    assert pages[0]["url"] == TARGET_URL
    assert sleep_calls == [6]

def test_get_internal_links_returns_only_same_domain_links():
    html = """
    <html>
        <body>
            <a href="/page/2/">Next</a>
            <a href="/tag/love/">Love tag</a>
            <a href="https://example.com/">External</a>
        </body>
    </html>
    """

    links = get_internal_links(html, TARGET_URL)

    assert "https://quotes.toscrape.com/page/2/" in links
    assert "https://quotes.toscrape.com/tag/love/" in links
    assert "https://example.com/" not in links


def test_extract_page_text_falls_back_to_general_text():
    html = """
    <html>
        <body>
            <h1>About page</h1>
            <p>This page has no quote blocks.</p>
        </body>
    </html>
    """

    text = extract_page_text(html)

    assert "About page" in text
    assert "This page has no quote blocks." in text