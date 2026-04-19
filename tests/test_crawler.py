from src.crawler import get_next_page_url, extract_page_text

def test_get_next_page_url():
    html = """
    <html>
        <body>
                <li class="next">
                    <a href="/page/2/">Next</a>
                </li>
        </body>
    </html>
    """
    assert get_next_page_url(html) == "https://quotes.toscrape.com/page/2/"

def test_get_next_page_url_no_next():
    html = """
    <html>
        <body>
                <li class="next">
                </li>
        </body>
    </html>
    """
    assert get_next_page_url(html) is None