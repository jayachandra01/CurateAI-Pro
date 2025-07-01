def deduplicate_links(link_list):
    seen = set()
    deduped = []
    for title, url in link_list:
        if url not in seen:
            deduped.append((title, url))
            seen.add(url)
    return deduped

from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_k=5):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_k)
    vectorizer.fit([text])
    return vectorizer.get_feature_names_out().tolist()

