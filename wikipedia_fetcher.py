import wikipedia

def fetch_wikipedia_links(topics, max_links=5):
    links = []
    for topic in topics:
        try:
            page = wikipedia.page(topic)
            links.append((topic, page.url))
            if len(links) >= max_links:
                break
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple meanings, try the first suggestion
            try:
                page = wikipedia.page(e.options[0])
                links.append((e.options[0], page.url))
            except Exception:
                continue
        except Exception:
            continue
    return links
