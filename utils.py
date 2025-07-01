def deduplicate_links(link_list):
    seen = set()
    deduped = []
    for title, url in link_list:
        if url not in seen:
            deduped.append((title, url))
            seen.add(url)
    return deduped
