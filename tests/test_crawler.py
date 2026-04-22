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

def test_get_next_page_url_no_next_link():
    html = """
    <html>
        <body>
                <p>No next link</p>
        </body>
    </html>
    """
    assert get_next_page_url(html) is None

def test_get_next_page_url_no_href():
    html = """
    <html>
        <body>
            <li class="next">
                <a>Next</a>
            </li>
        </body>
    </html>
    """
    assert get_next_page_url(html) is None

def test_get_next_page_url_no_anchor():
    html = """
    <html>
        <body>
                <li class="next">
                </li>
        </body>
    </html>
    """
    assert get_next_page_url(html) is None

def test_extract_page_text():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">"A test quote"</span>
                <span class="author">Test author</span>
                <div class="tags">
                    <a class="tag">life</a>
                    <a class="tag">truth</a>

                </div>
            </div>
        </body>
    </html>
    """
    text = extract_page_text(html)
    assert "A test quote" in text
    assert "Test author" in text
    assert "life" in text
    assert "truth" in text
