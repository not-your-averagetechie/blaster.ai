from pathlib import Path
import sys
import os

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import main
import streamlit.web.bootstrap as bootstrap

def handler(event, context):
    # Configure Streamlit for serverless
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'true'
    
    # Run the Streamlit app
    bootstrap.run(main, '', [], flag_options={})
