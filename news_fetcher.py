import requests
import streamlit as st
API_KEY = st.secrets["NEWSAPI_KEY"]


def fetch_news_articles(query, top_k=5):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&language=en&pageSize={top_k}&sortBy=relevancy&apiKey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [(a["title"], a["url"]) for a in articles if a.get("title") and a.get("url")]
    except Exception as e:
        print(f"[News Fetch Error]: {e}")
        return []
