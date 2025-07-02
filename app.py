# app.py
import streamlit as st
import traceback
from utils import extract_keywords, deduplicate_links, extract_text_from_url
from wikipedia_fetcher import fetch_wikipedia_links
from news_fetcher import fetch_news_articles
from scholar_fetcher import fetch_research_papers

st.set_page_config(page_title="CurateAI Pro Reading List Generator", page_icon="📚")
st.title("📚 CurateAI Pro Reading List Generator")

input_mode = st.radio("Choose Input Mode:", ["Text", "URL"], horizontal=True)

if input_mode == "Text":
    user_input = st.text_area("Enter a topic, sentence, or paragraph:", height=200)
else:
    user_input = st.text_input("Paste a URL (we'll extract the article):")

num_articles = st.slider("Number of reading suggestions:", 3, 10, 5)

if st.button("Generate Reading List") and user_input:
    with st.spinner("Fetching relevant reading materials..."):
        try:
            if input_mode == "URL":
                text = extract_text_from_url(user_input)
            else:
                text = user_input

            keywords = extract_keywords(text, top_k=3)
            query = keywords[0] if keywords else text

            wiki = fetch_wikipedia_links(query, top_k=num_articles)
            news = fetch_news_articles(query, top_k=num_articles)
            research = fetch_research_papers(query, top_k=num_articles)

            all_links = deduplicate_links(wiki + news + research)

            st.subheader("📌 Recommended Reading")
            if not all_links:
                st.warning("No relevant articles found. Try a different input.")
            else:
                for i, (title, url) in enumerate(all_links[:num_articles], 1):
                    st.markdown(f"{i}. [{title}]({url})")

        except Exception as e:
            st.error("An error occurred while generating the reading list.")
            st.exception(e)


