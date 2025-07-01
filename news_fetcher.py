import requests
import streamlit as st

API_KEY = st.secrets["api_keys"]["news_api_key"]

def fetch_news_articles(query, top_k=5):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&language=en&pageSize={top_k}&sortBy=publishedAt&apiKey={API_KEY}"
    )

    try:
        print(f"🔗 Final API URL:\n{url}")  # Helps you open this manually
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        print("🔍 Raw NewsAPI response:")
        print(data)  # Log full output

        articles = data.get("articles", [])
        return [(a["title"], a["url"]) for a in articles if a.get("title") and a.get("url")]

    except Exception as e:
        print(f"[News Fetch Error]: {e}")
        return []

