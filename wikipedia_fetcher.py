import wikipedia
import urllib.parse
from transformers import pipeline
import torch

generator = pipeline("text2text-generation", model="google/flan-t5-base", device=0 if torch.cuda.is_available() else -1)

def fetch_wikipedia_links(text, limit=5):
    prompt = f"Extract important topics from: {text}"
    response = generator(prompt, max_new_tokens=32, num_return_sequences=1)[0]['generated_text']
    keywords = [kw.strip() for kw in response.split(',') if kw.strip()]

    found = []
    seen_titles = set()
    for kw in keywords:
        try:
            search_results = wikipedia.search(kw, results=5)
            for title in search_results:
                if title in seen_titles:
                    continue
                try:
                    wikipedia.summary(title, sentences=1, auto_suggest=False)
                    url_title = urllib.parse.quote(title.replace(" ", "_"))
                    url = f"https://en.wikipedia.org/wiki/{url_title}"
                    found.append((title, url))
                    seen_titles.add(title)
                    break
                except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                    continue
        except:
            continue
        if len(found) >= limit:
            break
    return found
