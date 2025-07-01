import requests
import xml.etree.ElementTree as ET

def fetch_news_articles(query, top_k=5):
    try:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        results = []
        for item in items[:top_k]:
            title = item.find("title").text
            link = item.find("link").text
            results.append((title, link))

        if not results:
            st.warning("No news articles found from Google News.")
        return results

    except Exception as e:
        st.error("Error fetching news articles.")
        st.exception(e)
        return []


