from src.indexer import IndexType, tokenize

def get_index_entry(index: IndexType, word: str) -> dict[str,dict] | None:
    """
    Returns index entry for one word or none if word is not found
    """
    tokens = tokenize(word)
    if not tokens:
        return None
    
    return index.get(tokens[0])

def find_pages(index: IndexType, query: str) -> list[str]:
    """
    Returns all page URLs that contain all words in the query
    """
    tokens = tokenize(query)
    if not tokens:
        return []

    # remove duplicates
    unique_words = list(dict.fromkeys(tokens))

    for word in unique_words:
        if word not in index:
            return []
        
    matching_pages = set(index[unique_words[0]].keys())

    # only keep pages with all sets of words
    for word in unique_words[1:]:
        matching_pages &= set(index[word].keys())

    return sorted(matching_pages)