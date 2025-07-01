import requests
from bs4 import BeautifulSoup
import streamlit as st

def fetch_news_articles(query, top_k=5):
    try:
        # Google News search URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        url = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article")

        results = []
        seen = set()

        for article in articles:
            anchor = article.select_one("a")
            if not anchor:
                continue

            title = anchor.get_text(strip=True)
            link = anchor["href"]

            # Normalize Google redirect URLs
            if link.startswith("./articles/"):
                full_link = "https://news.google.com" + link[1:]
            elif link.startswith("http"):
                full_link = link
            else:
                continue

            if title and full_link and full_link not in seen:
                results.append((title, full_link))
                seen.add(full_link)

            if len(results) >= top_k:
                break

        if not results:
            st.warning("No news articles found from Google News.")
        return results

    except Exception as e:
        st.error("Error fetching news articles.")
        st.exception(e)
        return []


