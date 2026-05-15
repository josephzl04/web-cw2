import sys

from src.crawler import crawl_quotes
from src.indexer import build_inverted_index, save_index, load_index, IndexType
from src.search import find_pages, get_index_entry, find_phrase_pages, find_ranked_pages

INDEX_FILE = "data/index.json"
CURRENT_INDEX: IndexType | None = None

def print_usage():
    print("Commands:")
    print("  build")
    print("  load")
    print("  print <word>")
    print("  find <query>")
    print("  findphrase <phrase>")
    print("  rank <query>")
    print("  help")
    print("  exit")

def get_active_index():
    global CURRENT_INDEX
    if CURRENT_INDEX is None:
        try:
            CURRENT_INDEX = load_index(INDEX_FILE)
            print(f"Index loaded successfully from {INDEX_FILE}")
        except FileNotFoundError as error:
            print(f"Error loading index: {error}")
            return None
    return CURRENT_INDEX

def handle_build():
    """
    Crawls website, builds index and saves to file.
    """
    global CURRENT_INDEX
    print("Building index...")
    pages = crawl_quotes()
    index = build_inverted_index(pages)
    save_index(index, INDEX_FILE)
    CURRENT_INDEX = index
    print(f"Index built and saved to {INDEX_FILE}")

def handle_load():
    """
    Loads index.
    """
    global CURRENT_INDEX
    try:
        CURRENT_INDEX = load_index(INDEX_FILE)
        print(f"Index loaded successfully from {INDEX_FILE}")
    except FileNotFoundError as error:
        print(f"Error loading index: {error}")

def handle_print(word):
    """
    Prints index entry for a word.
    """
    index = get_active_index()
    if index is None:
        print(f"No index is currently loaded. Use 'build' or 'load' first.")
        return
    entry = get_index_entry(index, word)

    if entry is None:
        print(f"No entry found for word: {word}")
    else:
        print(f"Entry for word '{word}': {entry}")

def handle_find(query):
    """
    Print all pages that contain all words in the query.
    """
    index = get_active_index()

    if index is None:
        print(f"No index is currently loaded. Use 'build' or 'load' first.")
        return
    
    pages = find_pages(index, query)

    if pages:
        print(f"Pages matching '{query}':")
        for page in pages:
            print(f"  - {page}")
    else:
        print(f"No pages found matching query: '{query}'")

def handle_find_phrase(phrase):
    """
    Advanced feature 1 - Print all pages that contain the exact phrase.
    """
    index = get_active_index()
    
    if index is None:
        print(f"No index is currently loaded. Use 'build' or 'load' first.")
        return
    pages = find_phrase_pages(index, phrase)

    if pages:
        print(f"Pages matching exact phrase '{phrase}':")
        for page in pages:
            print(f"  - {page}")
    else:
        print(f"No pages found matching exact phrase: '{phrase}'")
    

def handle_rank(query):
    """
    Advanced feature 2 - Print pages ranked by TF-IDF score.
    """
    index = get_active_index()
    if index is None:
        print(f"No index is currently loaded. Use 'build' or 'load' first.")
        return
    
    ranked_pages = find_ranked_pages(index, query)

    if ranked_pages:
        print(f"Pages ranked for '{query}':")
        for page, score in ranked_pages:
            print(f"  - {page} (score: {score:.3f})")
    else:
        print(f"No ranked results found for query: '{query}'")

def execute_cmd(parts):
    if not parts:
        return
    
    command = parts[0].lower()

    if command == "build":
        handle_build()

    elif command == "load":
        handle_load()

    elif command == "print":
        if len(parts) < 2:
            print("Error: Please provide a word to print.")
            return
        handle_print(parts[1])

    elif command == "find":
        if len(parts) < 2:
            print("Error: Please provide a query to find.")
            return
        query = " ".join(parts[1:])
        handle_find(query)

    elif command == "findphrase":
        if len(parts) < 2:
            print("Error: Please provide a phrase to find.")
            return
        phrase = " ".join(parts[1:])
        handle_find_phrase(phrase)

    elif command == "rank":
        if len(parts) < 2:
            print("Error: Please provide a query to rank.")
            return
        query = " ".join(parts[1:])
        handle_rank(query)

    elif command == "help":
        print_usage()

    elif command == "exit":
        raise SystemExit
    
    else:
        print(f"Unknown command: {command}")
        print_usage()

def run_cli():
    print("Search Engine Tool")
    print("Type 'help' for a list of commands or 'exit' to quit.")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue

        parts = user_input.split()
        try:
            execute_cmd(parts)
        except SystemExit:
            print("\nExiting...")
            break
def main():

    if len(sys.argv) > 1:
        execute_cmd(sys.argv[1:])
    else:
        run_cli()

if __name__ == "__main__":
    main()
