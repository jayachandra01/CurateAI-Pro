import streamlit as st
import traceback

from wikipedia_fetcher import fetch_wikipedia_links
from news_fetcher import fetch_news_articles  # now handles NewsAPI + Google News
from utils import deduplicate_links, extract_keywords

st.set_page_config(page_title="CurateAI Pro Reading List Generator", page_icon="📚")
st.title("📚 CurateAI Pro Reading List Generator")
st.write("Enter a topic, sentence, or paragraph:")

# UI Inputs
text_input = st.text_area("Input", height=200)
num_articles = st.slider("Number of articles to fetch:", 3, 10, 5)

# Submit button
if st.button("Generate Reading List") and text_input:
    with st.spinner("Fetching relevant articles..."):
        try:
            # Step 1: Extract keywords from input
            keywords = extract_keywords(text_input, top_k=3)
            query = keywords[0] if keywords else text_input

            # Step 2: Fetch articles
            wiki_links = fetch_wikipedia_links(query, top_k=num_articles)
            news_links = fetch_news_articles(query, top_k=num_articles)

            # Step 3: Combine and deduplicate
            all_links = deduplicate_links(wiki_links + news_links)

            # Step 4: Display results
            if wiki_links:
                st.markdown("### 📚 Wikipedia Articles")
                for i, (title, url) in enumerate(wiki_links[:num_articles], 1):
                    st.markdown(f"{i}. [{title}]({url})")

            if news_links:
                st.markdown("### 📰 News Articles")
                for i, (title, url) in enumerate(news_links[:num_articles], 1):
                    st.markdown(f"{i}. [{title}]({url})")

            if not wiki_links and not news_links:
                st.warning("No articles found. Try a different query.")

            # Step 5: Unified list
            st.subheader("📌 Recommended Reading")
            for i, (title, url) in enumerate(all_links[:num_articles], 1):
                st.markdown(f"{i}. [{title}]({url})")

        except Exception as e:
            st.error("An error occurred while generating the reading list.")
            st.exception(e)


