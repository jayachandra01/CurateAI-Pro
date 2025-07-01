# utils.py

from typing import List, Tuple

def deduplicate_links(links: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Remove duplicate URLs from the list of (title, url) tuples.
    """
    seen = set()
    unique_links = []
    for title, url in links:
        if url not in seen:
            seen.add(url)
            unique_links.append((title, url))
    return unique_links
