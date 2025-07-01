import streamlit as st
from news_fetcher import fetch_news_articles
from wikipedia_fetcher import fetch_wikipedia_links
from utils import deduplicate_links

st.set_page_config(page_title="CurateAI Pro Reading List Generator", page_icon="📚")

st.title("📚 CurateAI Pro Reading List Generator")

st.write("Enter a topic, sentence, or paragraph:")

text_input = st.text_area("Input", height=200)
num_articles = st.slider("Number of articles to fetch:", 3, 10, 5)

if st.button("Generate Reading List") and text_input:
    with st.spinner("Fetching relevant articles..."):
        wiki_links = fetch_wikipedia_links(text_input, top_k=num_articles)
        news_links = fetch_news_articles(text_input, top_k=num_articles)
        all_links = deduplicate_links(wiki_links + news_links)

    st.subheader("📑 Recommended Reading")
    for i, (title, url) in enumerate(all_links[:num_articles], 1):
        st.markdown(f"{i}. [{title}]({url})")
