import os
from dotenv import load_dotenv
import streamlit as st
from newsapi import NewsApiClient
from pages.schema.NewsSchema import News
from pages.schema import hide_streamlit_style

load_dotenv()


st.set_page_config(
    page_title="UpSkilled News",
    page_icon="📰",
    menu_items={
        'Get Help': 'https://www.upskilled.ai',
        'Report a bug': "https://www.upskilled.ai",
        'About': "# News App made with Streamlit"
    }
)

st.write(hide_streamlit_style, unsafe_allow_html=True)

@st.cache_data
def get_news(query):
    newsapi = NewsApiClient(api_key=os.getenv("apiKey"))
    top_headlines = newsapi.get_everything(q=query, language='en')
    return News(**top_headlines)
    
    
def display(query):
    news = get_news(query)
    articles = news.articles
    
    sort_article = sorted(articles, key=lambda x: x.published, reverse=True)
    
    for article in sort_article:
        try:
            st.image(article.image)
            st.subheader(article.title)
            st.write(article.author, article.published.strftime("%d/%m/%Y, %H:%M:%S"))
            st.write(article.content)
            st.markdown(f'<a style="text-decoration: none;font-size:20px;" href="{article.url}">Read More</a>', unsafe_allow_html=True)
            st.divider()
        except Exception:
            continue

def main():
    st.header("NEWS 360")
    query_input = st.sidebar.text_input("Search", label_visibility="hidden")
    query = None
    if st.sidebar.button("Search"):
        query = query_input
    query = query or "India"
    display(query)


main()
    