import wikipedia

def fetch_wikipedia_links(query, top_k=5):
    try:
        search_results = wikipedia.search(query, results=top_k)
        links = []
        for title in search_results:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                links.append((page.title, page.url))
            except Exception:
                continue
        return links
    except Exception as e:
        print(f"[Wikipedia Error]: {e}")
        return []
