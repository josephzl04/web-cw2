from src.search import get_index_entry, find_pages

def test_get_index_entry_returns_entry_for_word():
    index = {
        "hello": {
            "page1": {
                "frequency": 2,
                "positions": [0, 2]
            }
        }
    }
    entry = get_index_entry(index, "hello")

    assert entry == {
        "page1": {
            "frequency": 2,
            "positions": [0, 2]
        }
    }

def test_get_index_entry_returns_none_for_missing_word():
    index = {
        "hello": {
            "page1": {
                "frequency": 2,
                "positions": [0, 2]
            }
        }
    }
    entry = get_index_entry(index, "world") is None

def test_find_pages_single_word():
    index = {
        "hello": {
            "page1": {
                "frequency": 2,
                "positions": [0, 2]
            },
            "page2": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    results = find_pages(index,"hello")
    assert results == ["page1", "page2"]

def test_find_pages_multiple_words():
    index = {
        "good": {
            "page1": {
                "frequency": 2,
                "positions": [0, 2]
            },
            "page2": {
                "frequency": 1,
                "positions": [0]
            }
        },
        "friends": {
            "page1": {
                "frequency": 1,
                "positions": [1]
            }
        }
    }

    results = find_pages(index,"good friends")
    assert results == ["page1"]

def test_find_pages_returns_empty_list_for_missing_word():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_pages(index, "hello world")

    assert results == []


def test_find_pages_returns_empty_list_for_empty_query():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_pages(index, "")

    assert results == []