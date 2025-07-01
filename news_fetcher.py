import requests
import streamlit as st
import feedparser

API_KEY = st.secrets["api_keys"].get("news_api_key", None)

def fetch_news_articles(query, top_k=5):
    if API_KEY:
        return fetch_from_newsapi(query, top_k)
    else:
        return fetch_from_google_news(query, top_k)


def fetch_from_newsapi(query, top_k):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&language=en&pageSize={top_k}&sortBy=publishedAt&apiKey={API_KEY}"
    )

    try:
        print(f"📰 Final API URL:\n{url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        status = data.get("status")
        if status != "ok":
            st.warning(f"NewsAPI returned non-ok status: {status}")
            return []

        articles = data.get("articles", [])
        results = [
            (a["title"].strip(), a["url"].strip())
            for a in articles if a.get("title") and a.get("url")
        ]
        if not results:
            st.warning("NewsAPI returned no usable articles.")
        return results

    except requests.exceptions.RequestException as e:
        print(f"[News Fetch Error]: {e}")
        st.error("Error fetching news articles. Try again later.")
        return []


def fetch_from_google_news(query, top_k):
    try:
        search_query = query.replace(" ", "+")
        rss_url = f"https://news.google.com/rss/search?q={search_query}&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(rss_url)

        articles = feed.entries[:top_k]
        results = [
            (entry.title, entry.link)
            for entry in articles if hasattr(entry, "title") and hasattr(entry, "link")
        ]
        if not results:
            st.warning("Google News returned no usable articles.")
        return results

    except Exception as e:
        print(f"[Google News Fetch Error]: {e}")
        st.error("Error fetching news from Google. Try again later.")
        return []


