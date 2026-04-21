import sys

from src.crawler import crawl_quotes
from src.indexer import build_inverted_index, save_index, load_index
from src.search import find_pages, get_index_entry

INDEX_FILE = "data/index.json"

def print_usage():
    print("Commands:")
    print("  build")
    print("  load")
    print("  print <word>")
    print("  find <query>")
    print("  help")
    print("  exit")

def handle_build():
    """Crawls website, builds index and saves to file"""
    print("Building index...")
    pages = crawl_quotes()
    index = build_inverted_index(pages)
    save_index(index, INDEX_FILE)
    print(f"Index built and saved to {INDEX_FILE}")

def handle_load():
    """Loads index"""
    try:
        load_index(INDEX_FILE)
        print(f"Index loaded successfully from {INDEX_FILE}")
    except FileNotFoundError as error:
        print(f"Error loading index: {error}")

def handle_print(word: str):
    """Prints index entry for a word"""
    try:
        index = load_index(INDEX_FILE)
    except FileNotFoundError as error:
        print(f"Error loading index: {error}")
        return
    entry = get_index_entry(index, word)

    if entry is None:
        print(f"No entry found for word: {word}")
    else:
        print(f"Entry for word '{word}': {entry}")

def handle_find(query: str):
    """Print all pages that contain all words in the query"""
    try:
        index = load_index(INDEX_FILE)
    except FileNotFoundError as error:
        print(f"Error loading index: {error}")
        return

    pages = find_pages(index, query)
    if pages:
        print(f"Pages matching '{query}':")
        for page in pages:
            print(f"  - {page}")
    else:
        print(f"No pages found matching query: '{query}'")

def execute_cmd(parts: list[str]):
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
