import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from ssl_config import configure_ssl

from chains import Chain
from portfolio import Portfolio
from utils import clean_text, suppress_warnings


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Initialize session state for url_input if it doesn't exist
    if 'url_input' not in st.session_state:
        st.session_state.url_input = "https://jobs.nike.com/job/R-33460"
    
    # Use the session state value as default
    url_input = st.text_input(
        "Enter a URL:", 
        value=st.session_state.url_input,
        key="url_input"
    )
    
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


@suppress_warnings
def main():
    # Configure SSL context
    configure_ssl()
    
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


if __name__ == "__main__":
    main()


