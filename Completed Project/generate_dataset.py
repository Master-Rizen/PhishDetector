import pandas as pd

# Example dataset with raw URLs and labels (1=phishing, 0=legitimate)
data = {
    'url': [
        # Phishing URLs
        "http://192.168.1.1/login.php",          # IP address
        "http://paypal.com@phishing-site.com",   # '@' sign
        "http://bit.ly/steal-password",          # URL shortener
        "http://fake-facebook-login.com",        # Hyphen in domain
        # Legitimate URLs
        "https://google.com",
        "https://github.com",
        "https://wikipedia.org",
        "https://microsoft.com"
    ],
    'label': [1, 1, 1, 1, 0, 0, 0, 0]
}

df = pd.DataFrame(data)
df.to_csv('url_dataset.csv', index=False)
print("Dataset generated with raw URLs!")