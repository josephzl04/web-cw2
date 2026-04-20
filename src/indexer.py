import json
import re
from pathlib import Path
from typing import Any

IndexType = dict[str, dict[str, dict[str, Any]]]

def tokenize(text: str) -> list[str]:
    """
    Makes it so search is not case sensitive
    """
    return re.findall(r"[a-zA-Z0-9]+(?:['-][a-zA-Z0-9]+)*", text.lower())

def add_page_to_index(index: IndexType, url: str, page_text: str) -> None:
    """
    Adds a page to the inverted index. If page exists, then update.
    For each token store frequency and position.

    """
    tokens = tokenize(page_text)
    for position, word in enumerate(tokens):
        if word not in index:
            index[word] = {}
      
        if url not in index[word]:
            index[word][url] = {
                "frequency": 0,
                "positions": []
            }

        index[word][url]["frequency"] += 1
        index[word][url]["positions"].append(position)

def build_inverted_index(pages: list[dict[str, str]]) -> IndexType:
    """
    Build an inverted index from list of crawled pages.
    """
    index: IndexType = {}
    for page in pages:
        url = page["url"]
        text = page["text"]
        add_page_to_index(index, url, text)
    return index

def save_index(index: IndexType, file_path: str = "data/index.json") -> None:
    """
    Save the inverted index to a JSON file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def load_index(file_path: str = "data/index.json") -> IndexType:
    """
    Load the inverted index from a JSON file.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Index file not found: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    # Example usage
    sample_pages = [
        {
            "url": "https://quotes.toscrape.com/page/1/",
            "text": 'Good friends, good books, and a sleepy conscience.'
        }
    ]
    index = build_inverted_index(sample_pages)
    save_index(index)
    print(index)