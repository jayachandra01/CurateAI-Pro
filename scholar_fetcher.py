import streamlit as st
import requests

SCHOLAR_KEY = st.secrets["api_keys"]["scholar_api_key"]

def fetch_scholar_links(query, limit=5):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google_scholar",
        "num": limit
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("organic_results", [])
        return [(item["title"], item["link"]) for item in results if "title" in item and "link" in item]
    except Exception as e:
        print(f"[Scholar Fetch Error]: {e}")
        return []
