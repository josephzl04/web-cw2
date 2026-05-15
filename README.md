# Search Engine Tool

## Project overview and purpose

The purpose of the project is to implement a search engine to crawl and gather information from the target website: 

"https://quotes.toscrape.com/"

The command line interface provides four commands:
- `build`
- `load`
- `print`
- `find`

These commands allow the user to crawl the target website, generate the inverted index, load the saved index, print the inverted index for a particular word, and search all pages containing a given query.

In addition to the four commands, this project also includes two advanced features:

- `findphrase` for exact phrase searching
- `rank` for TF-IDF ranked retrieval

`findphrase good friends` returns only pages containing the exact phrase, whereas `find good friends` returns pages containing both words anywhere on the page.

`rank` returns pages ranked by TF-IDF score so that more relevant pages appear first.


## Features
- Crawls all pages of the target website
- Respects a **6-second politeness window** between successive requests
- Builds an **inverted index** of words from crawled pages
- Stores page URL, word frequency, and token position
- Saves compiled index as a JSON file
- Loads saved index into memory
- Prints the index entry for a word
- Searches pages containing one or more query words
- Interactive CLI shell
- Automated tests with **pytest**
- Continuous integration through **GitHub Actions**

## Repository structure
```text
web-cw2/
    src/
        crawler.py
        indexer.py
        search.py
        main.py
    tests/
        test_crawler.py
        test_indexer.py
        test_search.py
    data/
        index.json
    requirements.txt
    README.md
```

## Tech stack

- **Language:** Python 3.11
- **HTTP requests:** `requests`
- **HTML parsing:** `beautifulsoup4`
- **Testing:** `pytest`
- **Coverage:** `coverage`
- **CI:** GitHub Actions


## Design
Inverted index is implemented as a nested dictionary because it is efficient for both indexing and retrieval.

Example structure:

```python
{
    "word": {
        "page_url": {
            "frequency": 2,
            "positions": [0,5]
        }
    }
}
```

This structure was chosen because:
- Direct lookup of a word is fast
- Direct lookup of a word's occurrences on a page is fast
- Frequency and positions can be updated easily during indexing
- Multi-word search can be implemented efficiently using set intersection
- Exact phrase search can be implemented using stored token positions


The compiled index is stored as a single JSON file because it is simple to save, easy to inspect and matches the coursework requirement of saving the whole index as a single file.

## Dependencies
This project uses

- `requests`
- `beautifulsoup4`
- `pytest`
- `coverage`

These dependencies can be installed using pip and the included requirements.txt file. 

## Installation instructions

### Prerequisites
- Python 3.11
- pip
- Git

---

### 1. Clone the repository
```bash
git clone https://github.com/josephzl04/web-cw2.git
cd web-cw2
```

### 2. Create a virtual environment
Windows
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
## How to run the program
Open terminal

Run
```bash
python -m src.main
```

This opens the command line interface where user can input commands.

## Usage Examples

### `build`

Crawls the website, builds the inverted index and saves to data/index.json

Input:
```text
> build
```
Output:
```
Building index...
Building index...
Crawling https://quotes.toscrape.com/...
Crawling https://quotes.toscrape.com/author/Albert-Einstein...
Crawling https://quotes.toscrape.com/author/Andre-Gide...
Crawling https://quotes.toscrape.com/author/Eleanor-Roosevelt...
Crawling https://quotes.toscrape.com/author/J-K-Rowling...
Crawling https://quotes.toscrape.com/author/Jane-Austen...
Crawling https://quotes.toscrape.com/author/Marilyn-Monroe...
Crawling https://quotes.toscrape.com/author/Steve-Martin...
Crawling https://quotes.toscrape.com/author/Thomas-A-Edison...
Crawling https://quotes.toscrape.com/login...
Crawling https://quotes.toscrape.com/page/2/...
...
Index built and saved to data/index.json
```

### `load`
Loads the saved index from disk into memory

Input:
```text
> load
```

Output:
```
Index loaded successfully from data/index.json
```

### `print <word>`
Prints the full inverted index entry for a word

Input:
```text
> print good
```

Output:
```
Index loaded successfully from data/index.json
Entry for word 'good': {'https://quotes.toscrape.com/': {'frequency': 1, 'positions': [94]}, 'https://quotes.toscrape.com/author/Albert-Einstein': {'frequency': 2, 'positions': [137, 195]}, 'https://quotes.toscrape.com/author/J-K-Rowling': {'frequency': 1, 'positions': [634]}, 'https://quotes.toscrape.com/page/2/': {'frequency': 3, 'positions': [22, 512, 514]}, 'https://quotes.toscrape.com/tag/aliteracy/page/1/': {'frequency': 1, 'positions': [13]}, 'https://quotes.toscrape.com/tag/books/': {'frequency': 3, 'positions': [13, 25, 27]}, 'https://quotes.toscrape.com/tag/books/page/1/': {'frequency': 3, 'positions': [13, 25, 27]}, 'https://quotes.toscrape.com/tag/classic/page/1/': {'frequency': 1, 'positions': [13]}, 'https://quotes.toscrape.com/tag/friends/': {'frequency': 3, 'positions': [22, 234, 236]}, 'https://quotes.toscrape.com/tag/friendship/': {'frequency': 2, 'positions': [24, 26]}, 'https://quotes.toscrape.com/tag/humor/': {'frequency': 1, 'positions': [13]}, 'https://quotes.toscrape.com/tag/humor/page/1/': {'frequency': 1, 'positions': [13]}, 'https://quotes.toscrape.com/tag/inspirational/': {'frequency': 1, 'positions': [95]}, 'https://quotes.toscrape.com/tag/inspirational/page/1/': {'frequency': 1, 'positions': [95]}, 'https://quotes.toscrape.com/tag/life/': {'frequency': 3, 'positions': [78, 288, 290]}, 'https://quotes.toscrape.com/tag/life/page/1/': {'frequency': 3, 'positions': [78, 288, 290]}, 'https://quotes.toscrape.com/tag/love/': {'frequency': 1, 'positions': [45]}, 'https://quotes.toscrape.com/tag/love/page/1/': {'frequency': 1, 'positions': [45]}, 'https://quotes.toscrape.com/page/1/': {'frequency': 1, 'positions': [94]}, 'https://quotes.toscrape.com/page/3/': {'frequency': 1, 'positions': [262]}, 'https://quotes.toscrape.com/tag/contentment/page/1/': {'frequency': 2, 'positions': [0, 2]}, 'https://quotes.toscrape.com/tag/friends/page/1/': {'frequency': 3, 'positions': [22, 234, 236]}, 'https://quotes.toscrape.com/tag/friendship/page/1/': {'frequency': 2, 'positions': [24, 26]}, 'https://quotes.toscrape.com/tag/heartbreak/page/1/': {'frequency': 1, 'positions': [22]}, 'https://quotes.toscrape.com/tag/sisters/page/1/': {'frequency': 1, 'positions': [22]}, 'https://quotes.toscrape.com/tag/writing/page/1/': {'frequency': 1, 'positions': [18]}, 'https://quotes.toscrape.com/author/Terry-Pratchett': {'frequency': 1, 'positions': [135]}, 'https://quotes.toscrape.com/author/George-Eliot': {'frequency': 1, 'positions': [61]}, 'https://quotes.toscrape.com/author/Ralph-Waldo-Emerson': {'frequency': 1, 'positions': [169]}, 'https://quotes.toscrape.com/tag/attributed-no-source/page/1/': {'frequency': 1, 'positions': [36]}, 'https://quotes.toscrape.com/tag/music/page/1/': {'frequency': 1, 'positions': [1]}, 'https://quotes.toscrape.com/tag/good/page/1/': {'frequency': 1, 'positions': [18]}, 'https://quotes.toscrape.com/page/6/': {'frequency': 1, 'positions': [47]}, 'https://quotes.toscrape.com/page/7/': {'frequency': 2, 'positions': [26, 236]}, 'https://quotes.toscrape.com/author/J-R-R-Tolkien': {'frequency': 1, 'positions': [434]}, 'https://quotes.toscrape.com/tag/alcohol/page/1/': {'frequency': 1, 'positions': [26]}, 'https://quotes.toscrape.com/page/9/': {'frequency': 1, 'positions': [69]}, 'https://quotes.toscrape.com/tag/integrity/page/1/': {'frequency': 1, 'positions': [29]}}
```

### `find <query>`
Returns all pages containing all words in the query

Input:
```
> find good friends
```

Output:
```
Pages matching 'good friends':
  - https://quotes.toscrape.com/author/George-Eliot
  - https://quotes.toscrape.com/author/J-K-Rowling
  - https://quotes.toscrape.com/page/2/
  - https://quotes.toscrape.com/page/6/
  - https://quotes.toscrape.com/tag/books/
  - https://quotes.toscrape.com/tag/books/page/1/
  - https://quotes.toscrape.com/tag/contentment/page/1/
  - https://quotes.toscrape.com/tag/friends/
  - https://quotes.toscrape.com/tag/friends/page/1/
  - https://quotes.toscrape.com/tag/friendship/
  - https://quotes.toscrape.com/tag/friendship/page/1/
  - https://quotes.toscrape.com/tag/heartbreak/page/1/
  - https://quotes.toscrape.com/tag/inspirational/
  - https://quotes.toscrape.com/tag/inspirational/page/1/
  - https://quotes.toscrape.com/tag/life/
  - https://quotes.toscrape.com/tag/life/page/1/
  - https://quotes.toscrape.com/tag/love/
  - https://quotes.toscrape.com/tag/love/page/1/
  - https://quotes.toscrape.com/tag/sisters/page/1/
```

### `findphrase <phrase>`
Returns only pages containing the exact phrase

Input:
```
> findphrase good friends
```

Output:
```
Pages matching exact phrase 'good friends':
  - https://quotes.toscrape.com/page/2/
  - https://quotes.toscrape.com/tag/books/
  - https://quotes.toscrape.com/tag/books/page/1/
  - https://quotes.toscrape.com/tag/contentment/page/1/
  - https://quotes.toscrape.com/tag/friends/
  - https://quotes.toscrape.com/tag/friends/page/1/
  - https://quotes.toscrape.com/tag/friendship/
  - https://quotes.toscrape.com/tag/friendship/page/1/
  - https://quotes.toscrape.com/tag/life/
  - https://quotes.toscrape.com/tag/life/page/1/
```

### `rank <query>`

Returns pages ranked by TF-IDF score

Input:
```
> rank good friends
```

Output:
```
Pages ranked for 'good friends':
  - https://quotes.toscrape.com/tag/friends/ (score: 36.134)
  - https://quotes.toscrape.com/tag/friends/page/1/ (score: 36.134)
  - https://quotes.toscrape.com/page/2/ (score: 33.022)
  - https://quotes.toscrape.com/tag/life/ (score: 26.796)
  - https://quotes.toscrape.com/tag/life/page/1/ (score: 26.796)
  - https://quotes.toscrape.com/tag/love/ (score: 18.270)
  - https://quotes.toscrape.com/tag/love/page/1/ (score: 18.270)
  - https://quotes.toscrape.com/tag/books/ (score: 17.459)
  - https://quotes.toscrape.com/tag/books/page/1/ (score: 17.459)
  - https://quotes.toscrape.com/tag/heartbreak/page/1/ (score: 15.157)
  - https://quotes.toscrape.com/tag/inspirational/ (score: 15.157)
  - https://quotes.toscrape.com/tag/inspirational/page/1/ (score: 15.157)
  - https://quotes.toscrape.com/tag/sisters/page/1/ (score: 15.157)
  - https://quotes.toscrape.com/tag/friendship/ (score: 14.752)
  - https://quotes.toscrape.com/tag/friendship/page/1/ (score: 14.752)
  - https://quotes.toscrape.com/tag/contentment/page/1/ (score: 11.639)
  - https://quotes.toscrape.com/page/6/ (score: 8.932)
  - https://quotes.toscrape.com/tag/courage/page/1/ (score: 6.225)
  - https://quotes.toscrape.com/author/George-Eliot (score: 5.820)
  - https://quotes.toscrape.com/author/J-K-Rowling (score: 5.820)
  - https://quotes.toscrape.com/author/Albert-Einstein (score: 5.414)
  - https://quotes.toscrape.com/page/7/ (score: 5.414)
  - https://quotes.toscrape.com/author/Douglas-Adams (score: 3.113)
  - https://quotes.toscrape.com/author/Harper-Lee (score: 3.113)
  - https://quotes.toscrape.com/author/Madeleine-LEngle (score: 3.113)
  - https://quotes.toscrape.com/author/Pablo-Neruda (score: 3.113)
  - https://quotes.toscrape.com/tag/novelist-quotes/page/1/ (score: 3.113)
  - https://quotes.toscrape.com/ (score: 2.707)
  - https://quotes.toscrape.com/author/J-R-R-Tolkien (score: 2.707)
  - https://quotes.toscrape.com/author/Ralph-Waldo-Emerson (score: 2.707)
  - https://quotes.toscrape.com/author/Terry-Pratchett (score: 2.707)
  - https://quotes.toscrape.com/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/page/3/ (score: 2.707)
  - https://quotes.toscrape.com/page/9/ (score: 2.707)
  - https://quotes.toscrape.com/tag/alcohol/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/aliteracy/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/attributed-no-source/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/classic/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/good/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/humor/ (score: 2.707)
  - https://quotes.toscrape.com/tag/humor/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/integrity/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/music/page/1/ (score: 2.707)
  - https://quotes.toscrape.com/tag/writing/page/1/ (score: 2.707)
```
## Testing instructions
Run full test suite using

```bash
python -m pytest -v
```


To run the test suite with coverage:
```bash
coverage run -m pytest
coverage report
```

This test covers:
- Single word search
- Multi word search
- Missing word and empty query behaviour
- Missing index file handling
- Saving and loading index
- Inverted index construction
- Tokenization (non case sensitive)
- Crawler pagination detection
- Crawler text extraction
- Frequency and position tracking
- Exact phrase search
- TF-IDF ranking
- Request failure handling
- Politeness window handling


## Continuous Integration (Github Actions)

Every push to main branch automatically runs the full Python test suite through GitHub Actions.

The workflow is defined in '.github/workflows/ci.yml'.

Test results are visible in the **Actions** tab on GitHub.


