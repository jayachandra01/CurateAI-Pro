import wikipediaapi

def fetch_wikipedia_links(query, top_k=5):
    try:
        wiki = wikipediaapi.Wikipedia('en')
        page = wiki.page(query)

        # If exact match page is missing, return empty
        if not page.exists():
            return []

        links = []
        for linked_title in page.links.keys():
            linked_page = wiki.page(linked_title)
            if linked_page.exists():
                links.append((linked_page.title, linked_page.fullurl))
            if len(links) >= top_k:
                break

        return links

    except Exception as e:
        print(f"[Wikipedia Error]: {e}")
        return []
