from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import streamlit.web.bootstrap as bootstrap
import os
from pathlib import Path
import sys

# Add app directory to path
sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()

@app.get("/{path:path}")
async def serve_streamlit(request: Request, path: str):
    # Configure minimal Streamlit settings
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # Import main only when needed
    from app.main import main
    
    # Run streamlit
    bootstrap.run(main, '', [], flag_options={})
