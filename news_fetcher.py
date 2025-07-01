import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_news_articles(query, top_k=5):
    try:
        # 1. Fetch from Google News RSS
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
            if title and link:
                titles.append(title)
                links.append(link)

        if not titles:
            return []

        # 2. Semantic re-ranking
        query_embedding = model.encode(query, convert_to_tensor=True)
        title_embeddings = model.encode(titles, convert_to_tensor=True)

        scores = util.pytorch_cos_sim(query_embedding, title_embeddings)[0]
        top_indices = scores.topk(top_k).indices

        results = [(titles[i], links[i]) for i in top_indices]
        return results

    except Exception as e:
        import streamlit as st
        st.error("Error fetching or ranking news articles.")
        st.exception(e)
        return []


