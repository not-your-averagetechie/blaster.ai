import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from ssl_config import configure_ssl
import webbrowser
import platform
import subprocess
import os
import urllib.parse

from chains import Chain
from portfolio import Portfolio
from utils import clean_text, suppress_warnings, create_mailto_link, extract_email, create_gmail_link


def open_gmail(to_email, subject, body):
    """Open Gmail compose in browser with prefilled content"""
    try:
        url = create_gmail_link(to_email, subject, body)
        # Try multiple methods to open the browser
        try:
            # Try default browser first
            webbrowser.open(url)
        except:
            # Fallback to specific browsers
            for browser in ['chrome', 'firefox', 'safari']:
                try:
                    webbrowser.get(browser).open(url)
                    break
                except:
                    continue
        st.markdown(f"**[Click here if Gmail doesn't open automatically]({url})**")
        return True
    except Exception as e:
        st.error(f"Failed to open Gmail: {str(e)}")
        return False

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Initialize session state for url_input if it doesn't exist
    if 'url_input' not in st.session_state:
        st.session_state.url_input = "https://cryptocurrencyjobs.co/engineering/nethermind-protocol-researcher/"
    
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
            raw_content = loader.load().pop().page_content
            data = clean_text(raw_content)
            contact_email = extract_email(raw_content) or "recruiter@company.com"
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                emails = llm.write_mail(job, links)
                
                st.subheader(f"Email Variations for {job.get('title', 'Position')}")
                
                for idx, email in enumerate(emails, 1):
                    with st.expander(f"Variation {idx}", expanded=(idx==1)):
                        col1, col2 = st.columns([10, 1])
                        with col1:
                            st.code(email, language='markdown')
                        with col2:
                            subject = f"Re: {job.get('title', 'Position')} Opening"
                            url = create_gmail_link(contact_email, subject, email)
                            st.markdown(
                                f"""
                                <a href='{url}' target='_blank' 
                                style='text-decoration:none; color:inherit;'>
                                    <button style='font-size:20px; border:none; 
                                    background:none; cursor:pointer;'>
                                        ✉️
                                    </button>
                                </a>
                                """, 
                                unsafe_allow_html=True
                            )
                        
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


@suppress_warnings
def main():
    try:
        # Configure SSL context
        configure_ssl()
        
        chain = Chain()
        portfolio = Portfolio()
        st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
        create_streamlit_app(chain, portfolio, clean_text)
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        if os.environ.get('VERCEL_ENV'):
            st.error("Note: Some features may be limited in the deployed version.")


if __name__ == "__main__":
    main()


