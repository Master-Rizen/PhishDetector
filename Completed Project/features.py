import re
import requests
from datetime import datetime
from urllib.parse import urlparse
import ipaddress
import logging
import whois

# Precompiled regex for performance
SHORTENING_SERVICES_REGEX = re.compile(
    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
    r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
    r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
    r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|"
    r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|"
    r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|"
    r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
    r"tr\.im|link\.zip\.net",
    re.IGNORECASE
)

def havingIP(url):
    try:
        ipaddress.ip_address(urlparse(url).netloc)
        return 1
    except:
        return 0

def haveAtSign(url):
    return 1 if "@" in url else 0

def getLength(url):
    return 1 if len(url) >= 54 else 0

def getDepth(url):
    path = urlparse(url).path
    return len([p for p in path.split('/') if p])

def redirection(url):
    pos = url.rfind('//')
    return 1 if (pos > 6) else 0

def httpDomain(url):
    return 1 if 'https' in urlparse(url).netloc else 0

def tinyURL(url):
    return 1 if SHORTENING_SERVICES_REGEX.search(url) else 0

def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

def get_whois_info(url):
    try:
        domain = urlparse(url).netloc
        return whois.whois(domain)
    except Exception as e:
        logging.warning(f"WHOIS lookup failed: {e}")
        return None

def web_traffic(url):
    # Placeholder (Alexa API is deprecated)
    return 0

def domainAge(domain_info):
    if not domain_info:
        return 1
    try:
        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        age = (expiration_date - creation_date).days
        return 1 if (age / 30) < 6 else 0
    except:
        return 1

def domainEnd(domain_info):
    if not domain_info:
        return 1
    try:
        expiration_date = domain_info.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        days_left = (expiration_date - datetime.now()).days
        return 1 if (days_left / 30) < 6 else 0
    except:
        return 1

def fetch_url_content(url):
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )
        return response
    except:
        return None

def iframe(response):
    if not response:
        return 1
    return 0 if re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1

def mouseOver(response):
    if not response:
        return 1
    return 1 if re.findall("<script>.+onmouseover.+</script>", response.text) else 0

def rightClick(response):
    if not response:
        return 1
    return 0 if re.findall(r"event.button ?== ?2", response.text) else 1

def forwarding(response):
    if not response:
        return 1
    return 1 if len(response.history) > 2 else 0

def featureExtraction(url):
    features = []
    # URL-based features
    features.extend([
        havingIP(url),
        haveAtSign(url),
        getLength(url),
        getDepth(url),
        redirection(url),
        httpDomain(url),
        tinyURL(url),
        prefixSuffix(url),
    ])
    
    # Domain-based features
    domain_info = get_whois_info(url)
    features.extend([
        1 if not domain_info else 0,
        web_traffic(url),
        domainAge(domain_info),
        domainEnd(domain_info),
    ])
    
    # HTML/JS-based features
    response = fetch_url_content(url)
    features.extend([
        iframe(response),
        mouseOver(response),
        rightClick(response),
        forwarding(response),
    ])
    
    return features