from src.indexer import load_index, tokenize, add_page_to_index, build_inverted_index, save_index
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

def test_build_inverted_index():
    pages = [
        {
            "url": "https://quotes.toscrape.com",
            "text": "hello world hello"
        }
    ]

    index = build_inverted_index(pages)
    url = "https://quotes.toscrape.com"
    assert index["hello"][url]["frequency"] == 2
    assert index["hello"][url]["positions"] == [0, 2]
    assert index["world"][url]["frequency"] == 1
    assert index["world"][url]["positions"] == [1]

def test_save_and_load_index(tmp_path):
    index = {
        "hello": {
            "https://quotes.toscrape.com": {
                "frequency": 2,
                "positions": [0, 2]
            }
        }
    }
    file_path = tmp_path / "index.json"
    save_index(index, str(file_path))

    loaded_index = load_index(str(file_path))
    assert loaded_index == index

def test_load_index_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.json"
    try:
        load_index(str(missing_file))
        assert False
    except FileNotFoundError:
        assert True