import requests
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_research_papers(query, top_k=5):
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=20&fields=title,url"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        papers = data.get("data", [])

        if not papers:
            return []

        titles = [paper["title"] for paper in papers]
        urls = [paper.get("url", "") for paper in papers]

        # Rank papers by semantic similarity to the query
        query_embedding = model.encode(query, convert_to_tensor=True)
        title_embeddings = model.encode(titles, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, title_embeddings)[0]

        top_indices = scores.topk(top_k).indices
        results = [(titles[i], urls[i]) for i in top_indices]

        return results

    except Exception as e:
        import streamlit as st
        st.error("Error fetching research papers.")
        st.exception(e)
        return []
