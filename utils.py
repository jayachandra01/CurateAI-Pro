def deduplicate_results(results):
    seen = set()
    unique = []
    for title, url in results:
        if url not in seen:
            unique.append((title, url))
            seen.add(url)
    return unique
