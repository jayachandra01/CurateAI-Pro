import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer, util

# Load transformer model for semantic re-ranking
model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_news_articles(query, top_k=5):
    try:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        titles = []
        links = []

        for item in items:
            title = item.find("title").text
            link = item.find("link").text
            if title and link and "news.google.com" not in link:
                titles.append(title)
                links.append(link)

        if not titles:
            return []

        # Semantic similarity scoring
        query_embedding = model.encode(query, convert_to_tensor=True)
        title_embeddings = model.encode(titles, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, title_embeddings)[0]
        top_indices = scores.topk(top_k).indices

        return [(titles[i], links[i]) for i in top_indices]

    except Exception as e:
        import streamlit as st
        st.error("Error fetching or ranking news articles.")
        st.exception(e)
        return []



