from sklearn.feature_extraction.text import TfidfVectorizer
from newspaper import Article

def deduplicate_links(link_list):
    seen = set()
    deduped = []
    for title, url in link_list:
        if url not in seen:
            deduped.append((title, url))
            seen.add(url)
    return deduped

def extract_keywords(text, top_k=5):
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=top_k)
        vectorizer.fit([text])
        return vectorizer.get_feature_names_out().tolist()
    except Exception:
        return []

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception:
        return url  # fallback to using the URL string if parsing fails


