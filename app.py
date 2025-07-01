import streamlit as st
from modules.wikipedia_fetcher import fetch_wikipedia_links
from modules.scholar_fetcher import fetch_scholar_links
from modules.news_fetcher import fetch_news_links
from modules.utils import deduplicate_results

st.set_page_config(page_title="CurateAI Pro", page_icon="📚")

st.title("CurateAI Pro: Intelligent Article Recommender")
st.write("Paste a topic or paragraph. Get relevant Wikipedia, Scholar, and News links.")

input_text = st.text_area("Enter your topic or paragraph:", height=150)
num_results = st.slider("Number of suggestions per source", 1, 10, 5)

sources = st.multiselect("Select Sources", ["Wikipedia", "Google Scholar", "News"], default=["Wikipedia"])

if st.button("🔍 Recommend") and input_text.strip():
    with st.spinner("Fetching relevant articles..."):
        all_links = []

        if "Wikipedia" in sources:
            all_links += fetch_wikipedia_links(input_text, num_results)
        if "Google Scholar" in sources:
            all_links += fetch_scholar_links(input_text, num_results)
        if "News" in sources:
            all_links += fetch_news_links(input_text, num_results)

        all_links = deduplicate_results(all_links)

        if all_links:
            st.success("Here are your recommendations:")
            for idx, (title, url) in enumerate(all_links, 1):
                st.markdown(f"{idx}. [{title}]({url})")
        else:
            st.warning("No relevant links found. Try refining your input.")
