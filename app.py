
import streamlit as st
import requests
from transformers import pipeline
import wikipedia
import urllib.parse

st.set_page_config(page_title="CurateAI Pro", page_icon="📚")
st.title("CurateAI Pro: Smart Reading List Generator")
st.write("Enter a topic, sentence, or paragraph:")

input_text = st.text_area("Input", height=150)
num_articles = st.slider("Number of articles to fetch:", 3, 10, 5)

api_key = st.secrets["newsapi"]["key"] if "newsapi" in st.secrets else None

generator = pipeline("text2text-generation", model="google/flan-t5-base")

def get_keywords(text):
    prompt = f"Extract important topics from: {text}"
    response = generator(prompt, max_new_tokens=32, num_return_sequences=1)[0]['generated_text']
    return [kw.strip() for kw in response.split(',') if kw.strip()]

def get_wikipedia_links(keywords, limit):
    links = []
    seen = set()
    for kw in keywords:
        try:
            results = wikipedia.search(kw, results=3)
            for title in results:
                if title in seen:
                    continue
                try:
                    summary = wikipedia.summary(title, sentences=1)
                    url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                    links.append((title, url))
                    seen.add(title)
                    break
                except:
                    continue
        except:
            continue
        if len(links) >= limit:
            break
    return links

def get_news_articles(keywords, limit):
    if not api_key:
        return []
    articles = []
    headers = {"Authorization": api_key}
    for kw in keywords:
        url = f"https://newsapi.org/v2/everything?q={urllib.parse.quote(kw)}&language=en&pageSize=3"
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                for a in r.json().get("articles", []):
                    articles.append((a["title"], a["url"]))
        except:
            continue
        if len(articles) >= limit:
            break
    return articles[:limit]

if st.button("Generate Reading List"):
    if not input_text.strip():
        st.warning("Please enter a valid input.")
    else:
        with st.spinner("Analyzing and fetching links..."):
            try:
                keywords = get_keywords(input_text)
                wiki_links = get_wikipedia_links(keywords, num_articles)
                news_links = get_news_articles(keywords, num_articles)

                if wiki_links:
                    st.subheader("Wikipedia Articles")
                    for i, (title, url) in enumerate(wiki_links, 1):
                        st.markdown(f"{i}. [{title}]({url})")

                if news_links:
                    st.subheader("News & Articles")
                    for i, (title, url) in enumerate(news_links, 1):
                        st.markdown(f"{i}. [{title}]({url})")

                if not wiki_links and not news_links:
                    st.warning("No relevant content found. Try rephrasing the input.")
            except Exception as e:
                st.error(f"Error: {e}")
