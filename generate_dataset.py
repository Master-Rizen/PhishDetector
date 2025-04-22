import pandas as pd

# Expanded dataset with more phishing and legitimate URLs, including HTTPS phishing examples
data = {
    'url': [
        # Phishing URLs
        "http://192.168.1.1/login.php",              # IP address
        "http://paypal.com@phishing-site.com",       # '@' sign
        "http://bit.ly/steal-password",              # URL shortener
        "http://fake-facebook-login.com",            # Hyphen in domain
        "https://secure-paypal-login.com",           # HTTPS phishing with hyphen
        "https://bankofamerica-verify.com",          # HTTPS phishing with hyphen
        "https://phish-get-password/",               # Your test URL
        "https://login-secure-netflix.com",          # HTTPS phishing with hyphen
        # Legitimate URLs
        "https://google.com",                        # Legitimate
        "https://github.com",                        # Legitimate
        "https://wikipedia.org",                     # Legitimate
        "https://microsoft.com",                     # Legitimate
        "https://paypal.com",                        # Legitimate
        "https://facebook.com",                      # Legitimate
        "https://amazon.com",                        # Legitimate
        "https://netflix.com"                        # Legitimate
    ],
    'label': [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)
df.to_csv('url_dataset.csv', index=False)
print("Dataset generated with expanded URLs!")