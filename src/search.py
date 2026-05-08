from src.indexer import tokenize

def get_index_entry(index, word):
    """
    Returns index entry for one word or none if word is not found
    """
    tokens = tokenize(word)
    if not tokens:
        return None
    
    return index.get(tokens[0])

def find_pages(index, query):
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

def find_phrase_pages(index, phrase):
    """
    Returns all page URLs that contain the exact phrase
    """
    words = tokenize(phrase)
    if not words:
        return []

    for word in words:
        if word not in index:
            return []
    
    # Pages must contain every word in the phrase
    matching_pages = set(index[words[0]].keys())
    for word in words[1:]:
        matching_pages &= set(index[word].keys())
    
    phrase_matches = []

    for page in sorted(matching_pages):
        first_word_positions = index[words[0]][page]["positions"]
        other_position_sets = [
            set(index[word][page]["positions"])
            for word in words[1:]
        ]

        for start_pos in first_word_positions:
            if all((start_pos + offset) in other_position_sets[offset - 1]
                   for offset in range(1, len(words))):
                phrase_matches.append(page)
                break

    return phrase_matches