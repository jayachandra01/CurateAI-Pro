import streamlit as st

from wikipedia_fetcher import fetch_wikipedia_links
from scholar_fetcher import fetch_scholar_links
from news_fetcher import fetch_news_links
from utils import deduplicate_links

st.set_page_config(page_title="CurateAI Pro - Reading List Generator", layout="centered")

st.title("CurateAI Pro: Multimodal Reading List Generator")
st.markdown("Enter a topic, sentence, or paragraph:")

input_text = st.text_area("Input", height=200)

num_articles = st.slider("Number of articles to fetch:", 3, 10, 5)

if st.button("Generate Reading List"):
    if not input_text.strip():
        st.warning("Please enter a valid input.")
    else:
        with st.spinner("Generating reading list..."):
            wiki_links = fetch_wikipedia_links(input_text, num_articles)
            scholar_links = fetch_scholar_links(input_text, num_articles)
            news_links = fetch_news_links(input_text, num_articles)

            all_links = wiki_links + scholar_links + news_links
            curated_links = deduplicate_links(all_links)[:num_articles]

        if curated_links:
            st.subheader("📚 Recommended Reading")
            for i, (title, url) in enumerate(curated_links, 1):
                st.markdown(f"{i}. [{title}]({url})")
        else:
            st.warning("No relevant articles found. Please try again with different input.")

