import requests
import streamlit as st

API_KEY = st.secrets["api_keys"]["news_api_key"]

def fetch_news_articles(query, top_k=5):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&language=en&pageSize={top_k}&sortBy=publishedAt&apiKey={API_KEY}"
    )

    try:
        print(f"🧭 Final API URL:\n{url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        status = data.get("status")
        if status != "ok":
            st.warning(f"NewsAPI returned non-ok status: {status}")
            return []

        articles = data.get("articles", [])
        results = []

        for a in articles:
            title = a.get("title")
            url = a.get("url")
            if title and url:
                results.append((title.strip(), url.strip()))

        if not results:
            st.warning("NewsAPI returned no usable articles.")

        return results

    except requests.exceptions.RequestException as e:
        print(f"[News Fetch Error]: {e}")
        st.error("Error fetching news articles. Try again later.")
        return []

