import requests
import toml

# Load API key from config
config = toml.load("config.toml")
NEWS_API_KEY = config["api_keys"]["news_api_key"]

def fetch_news_articles(query, max_articles=5):
    url = (
        f"https://newsapi.org/v2/everything?q={query}&sortBy=relevancy"
        f"&language=en&pageSize={max_articles}&apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [(article["title"], article["url"]) for article in articles]
    except Exception as e:
        print("News fetch error:", e)
        return []
