import streamlit as st
from transformers import pipeline
from wikiscraper import WikiScraper
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse', False)

if "button" not in st.session_state:
    st.session_state["button"] = False

if "wiki_button" not in st.session_state:
    st.session_state["wiki_button"] = False

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
st.title("Text Summarizer")

tab1, tab2, tab3 = st.tabs(["Text", "File", "Wiki"])

with tab1:
    txt = st.text_area(
        "Text to analyze:",
        )

    if st.button("Summarize!", key=1):
        st.session_state["button"] = True
        st.session_state["wiki_button"] = False

with tab2:
    uploaded_file = st.file_uploader("Choose a file")

    if st.button("Summarize!", key=2):
        txt = uploaded_file.getvalue().decode("utf-8")
        st.session_state["button"] = True
        st.session_state["wiki_button"] = False

with tab3:
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    }
    scraper = WikiScraper(header)
    wiki_url = st.text_input(
        "Enter Wiki URL:",
    )

    if st.button("Summarize!", key=3):
        txt, link_list = scraper.scrape(wiki_url)
        st.session_state["button"] = True
        st.session_state["wiki_button"] = True

if st.session_state["button"]:
    st.header('Original Text:', divider='rainbow')
    st.markdown(txt)

    st.header('Summarized Text:', divider='rainbow')
    summarized_text = summarizer(txt, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    st.markdown(summarized_text)

    st.header('Analysis:', divider='rainbow')

    if st.session_state["wiki_button"]:
        col1, col2 = st.columns([2, 1])

        with col1:
            wordcloud = WordCloud().generate(txt)

            # Display the generated image:
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()

        with col2:
            st.table({'URL': link_list})
    else:
        wordcloud = WordCloud().generate(txt)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()  
