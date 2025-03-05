import re
import warnings
import urllib.parse
from functools import wraps

def suppress_warnings(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", module="urllib3")
            return func(*args, **kwargs)
    return wrapper

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def create_mailto_link(to_email, subject, body):
    """Create a standard mailto link with prefilled data"""
    params = {
        'subject': urllib.parse.quote(subject),
        'body': urllib.parse.quote(body)
    }
    mailto = f"mailto:{to_email}?subject={params['subject']}&body={params['body']}"
    return mailto

def create_gmail_link(to_email, subject, body):
    """Create a Gmail compose URL with prefilled data"""
    # Use compose interface directly
    base_url = "https://mail.google.com/mail/?view=cm"
    params = {
        'to': to_email,
        'su': subject,  # Gmail uses 'su' for subject
        'body': body
    }
    # Properly encode parameters and create full URL
    return base_url + '&' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

def extract_email(text):
    """Extract email from text using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found = re.findall(email_pattern, text)
    return found[0] if found else None