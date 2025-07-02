import wikipediaapi
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
wiki_wiki = wikipediaapi.Wikipedia('en')

def fetch_wikipedia_links(query, top_k=5):
    try:
        search_results = wiki_wiki.search(query)

        if not search_results:
            return []

        titles = search_results[:top_k * 2]  # Fetch extra to rerank better
        embeddings = model.encode(titles, convert_to_tensor=True)
        query_embedding = model.encode(query, convert_to_tensor=True)

        scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        top_indices = scores.topk(top_k).indices

        results = []
        for i in top_indices:
            title = titles[i]
            page = wiki_wiki.page(title)
            if page.exists():
                results.append((title, page.fullurl))

        return results
    except Exception as e:
        import streamlit as st
        st.error("Error fetching Wikipedia articles.")
        st.exception(e)
        return []
