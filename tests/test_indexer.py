from src.indexer import tokenize, add_page_to_index, build_inverted_index

def test_tokenize_makes_lowercase():
    text = "hello WORLD"
    assert tokenize(text) == ["hello", "world"]

def test_add_page_to_index_tracks_frequency_and_positions():
    index = {}
    url = "https://quotes.toscrape.com/page/1/"
    page_text = "hello world hello"
    add_page_to_index(index, url, page_text)

    assert index == {
        "hello": {
            url: {
                "frequency": 2,
                "positions": [0, 2]
            }
        },
        "world": {
            url: {
                "frequency": 1,
                "positions": [1]
            }
        }
    }