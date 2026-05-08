from src.search import get_index_entry, find_pages, find_phrase_pages, find_ranked_pages

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
    assert get_index_entry(index, "world") is None

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

    results = find_pages(index, "hello")
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

    results = find_pages(index, "good friends")
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

def test_get_index_entry_returns_none_for_empty_input():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    assert get_index_entry(index, "") is None


def test_find_pages_ignores_duplicate_query_words():
    index = {
        "hello": {
            "page1": {"frequency": 2, "positions": [0, 2]}
        }
    }

    assert find_pages(index, "hello hello") == ["page1"]


def test_find_phrase_pages_returns_matching_page():
    index = {
        "good": {
            "page1": {"frequency": 1, "positions": [0]},
            "page2": {"frequency": 1, "positions": [5]}
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [1]},
            "page2": {"frequency": 1, "positions": [9]}
        }
    }

    results = find_phrase_pages(index, "good friends")
    assert results == ["page1"]

def test_find_phrase_pages_returns_empty_list_when_words_are_not_adjacent():
    index = {
        "good": {
            "page1": {"frequency": 1, "positions": [0]}
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [3]}
        }
    }

    results = find_phrase_pages(index, "good friends")
    assert results == []

def test_find_phrase_pages_returns_empty_list_for_missing_word():
    index = {
        "good": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    results = find_phrase_pages(index, "good friends")
    assert results == []

def test_find_ranked_pages_orders_results_by_tfidf_score():
    index = {
        "good": {
            "page1": {"frequency": 3, "positions": [0, 1, 2]},
            "page2": {"frequency": 1, "positions": [0]}
        },
        "rare": {
            "page1": {"frequency": 1, "positions": [3]}
        },
        "other": {
            "page3": {"frequency": 2, "positions": [0, 1]}
        }
    }

    results = find_ranked_pages(index, "good rare")

    assert results[0][0] == "page1"
    assert results[1][0] == "page2"
    assert results[0][1] > results[1][1]

def test_find_ranked_pages_returns_empty_list_for_empty_query():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    assert find_ranked_pages(index, "") == []

def test_find_ranked_pages_returns_empty_list_for_missing_words():
    index = {
        "hello": {
            "page1": {"frequency": 1, "positions": [0]}
        }
    }

    assert find_ranked_pages(index, "missing words") == []