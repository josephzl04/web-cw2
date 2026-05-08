# Project Overview and purpose
Purpose of the project is to implement a search engine to crawl and gather information from the target website: "https://quotes.toscrape.com/"

There are command line interface provides four commands:
- Build
- Load
- Print
- Find

These commands allow the user to crawl the target website, generate the inverted index, load the saved index, print the inverted index for a particular word, and search all pages containing given query phrase.

## Features
- Crawls all pages of the target website
- Respects a 6 second politeness window between successive requests
- Builds an inverted index of words from crawled pages
- Storing page URL, word frequency, token position
- Saves compiled index as a JSON file
- Loads saved index into memory
- Prints the index entry for a word
- Search pages containing one or more query words
- Interactive CLI shell
- Automated tests with pytest
- Continuous integration through Github Actions

## Repository structure
repository-name/
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
        [compiled index file]
    requirements.txt
    README.md

# Tech stack

# Design
Inverted index is implemented as a nested dictionary because it is efficient for both indexing and retrieveil.

Stored as a single JSON file because it is simple to save, easy to inspect and matches cw requirement of saving the whole index as a single file.

# Dependencies
This project uses
- requests
- beautifulsoup4
- pytest
These dependencies can be installed using pip and the included requirements.txt file. (instructions included below in Installation steps)

# Installation steps

# Prerequites
- Python 3.11
- Pip
- Git

# 1. Clone the repository
```bash
git clone https://github.com/josephzl04/web-cw2.git
cd web-cw2
```

# 2. Create a virtual environment
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
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# How to run the program
Open terminal
Run python -m src.main
This opens the command line interface where user can input commands.

# Usage Examples
> Build
Crawls the website, builds the inverted index and saves to data/index.json

Output:
Building index...
Crawling https://quotes.toscrape.com/...
Crawling https://quotes.toscrape.com/page/2/...
Crawling https://quotes.toscrape.com/page/3/...
Crawling https://quotes.toscrape.com/page/4/...
Crawling https://quotes.toscrape.com/page/5/...
Crawling https://quotes.toscrape.com/page/6/...
Crawling https://quotes.toscrape.com/page/7/...
Crawling https://quotes.toscrape.com/page/8/...
Crawling https://quotes.toscrape.com/page/9/...
Crawling https://quotes.toscrape.com/page/10/...
Index built and saved to data/index.json

>Load
Loads the saved index from disk into memory

Output:
Index loaded successfully from data/index.json

> print good
Prints the full inverted index entry for a word

Output:
Index loaded successfully from data/index.json
Entry for word 'good': {'https://quotes.toscrape.com/': {'frequency': 1, 'positions': [94]}, 'https://quotes.toscrape.com/page/2/': {'frequency': 3, 'positions': [22, 512, 514]}, 'https://quotes.toscrape.com/page/3/': {'frequency': 1, 'positions': [262]}, 'https://quotes.toscrape.com/page/6/': {'frequency': 1, 'positions': [47]}, 'https://quotes.toscrape.com/page/7/': {'frequency': 2, 'positions': [26, 236]}, 'https://quotes.toscrape.com/page/9/': {'frequency': 1, 'positions': [69]}}

> find good friends
Returns all pages containing all words in the query

Output:
Pages matching 'good friends':
  - https://quotes.toscrape.com/page/2/
  - https://quotes.toscrape.com/page/6/


# Testing instructions
Run full test suite using
python -m pytest -v is this only windows or

This test covers:
- Single word search
- Multi word search
- Missing word and empty query behaviour
- Missing index file handling
- Saving and loading index
- Inverted Index construction
- Tokenization (non case sensitive)
- Crawler pagination detection
- Crawler text extraction
- Frequency and position tracking

# Continuous Integration (Github Actions)
Every push to main branch automatically runs the full python tests through GitHub Actions.
The workflow is defined in '.github/workflows/ci.yml'.
Test results are visible in the **Actions** tab on GitHub.

