import ssl
import certifi
import urllib3

def configure_ssl():
    # Create a default SSL context using system certificates
    context = ssl.create_default_context(cafile=certifi.where())
    
    # Configure for TLS 1.2+
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1
    
    # Set up urllib3 to use the configured context
    urllib3.disable_warnings()
    urllib3.util.ssl_.SSL_CONTEXT_VERIFIED_CERTS = context
    
    return context
