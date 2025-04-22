import re
import math
from collections import Counter
from urllib.parse import urlparse
import ipaddress
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    """Check if the URL uses an IP address instead of a domain name."""
    try:
        ipaddress.ip_address(urlparse(url).netloc)
        logger.info(f"havingIP for {url}: 1")
        return 1
    except:
        logger.info(f"havingIP for {url}: 0")
        return 0

def haveAtSign(url):
    """Check if the URL contains an '@' symbol."""
    result = 1 if "@" in url else 0
    logger.info(f"haveAtSign for {url}: {result}")
    return result

def getLength(url):
    """Check if the URL length is greater than or equal to 54 characters."""
    result = 1 if len(url) >= 54 else 0
    logger.info(f"getLength for {url}: {result}")
    return result

def getDepth(url):
    """Calculate the depth of the URL path."""
    try:
        path = urlparse(url).path
        result = len([p for p in path.split('/') if p])
        logger.info(f"getDepth for {url}: {result}")
        return result
    except:
        logger.info(f"getDepth for {url}: 0 (error)")
        return 0

def redirection(url):
    """Check if the URL has a redirection (// in the path)."""
    pos = url.rfind('//')
    result = 1 if (pos > 6) else 0
    logger.info(f"redirection for {url}: {result}")
    return result

def httpDomain(url):
    """Check if 'https' is in the domain part of the URL."""
    try:
        result = 1 if 'https' in urlparse(url).netloc else 0
        logger.info(f"httpDomain for {url}: {result}")
        return result
    except:
        logger.info(f"httpDomain for {url}: 0 (error)")
        return 0

def tinyURL(url):
    """Check if the URL uses a known URL shortening service."""
    result = 1 if SHORTENING_SERVICES_REGEX.search(url) else 0
    logger.info(f"tinyURL for {url}: {result}")
    return result

def suspicious_keywords(url):
    """Check for suspicious keywords in the domain."""
    suspicious = ['phish', 'login', 'secure', 'verify', 'account']
    domain = urlparse(url).netloc.lower()
    return 1 if any(keyword in domain for keyword in suspicious) else 0

def prefixSuffix(url):
    """Check if the domain contains a '-' symbol."""
    try:
        result = 1 if '-' in urlparse(url).netloc else 0
        logger.info(f"prefixSuffix for {url}: {result}")
        return result
    except:
        logger.info(f"prefixSuffix for {url}: 0 (error)")
        return 0

def subdomain_count(url):
    """Count the number of subdomains in the URL."""
    try:
        domain = urlparse(url).netloc
        parts = domain.split('.')
        result = len(parts) - 2 if len(parts) > 2 else 0
        logger.info(f"subdomain_count for {url}: {result}")
        return result
    except:
        logger.info(f"subdomain_count for {url}: 0 (error)")
        return 0

def uses_https(url):
    """Check if the URL uses HTTPS."""
    try:
        result = 1 if urlparse(url).scheme == 'https' else 0
        logger.info(f"uses_https for {url}: {result}")
        return result
    except:
        logger.info(f"uses_https for {url}: 0 (error)")
        return 0

def has_port(url):
    """Check if the URL specifies a port number."""
    try:
        result = 1 if urlparse(url).port else 0
        logger.info(f"has_port for {url}: {result}")
        return result
    except:
        logger.info(f"has_port for {url}: 0 (error)")
        return 0

def special_char_count(url):
    """Count special characters like %, ?, &, # in the URL."""
    try:
        special_chars = ['%', '?', '&', '#']
        result = sum(url.count(char) for char in special_chars)
        logger.info(f"special_char_count for {url}: {result}")
        return result
    except:
        logger.info(f"special_char_count for {url}: 0 (error)")
        return 0

def domain_entropy(url):
    """Calculate the entropy of the domain name."""
    try:
        domain = urlparse(url).netloc
        if not domain:
            logger.info(f"domain_entropy for {url}: 0 (no domain)")
            return 0
        freq = Counter(domain)
        length = len(domain)
        entropy = -sum((count / length) * math.log2(count / length) for count in freq.values())
        logger.info(f"domain_entropy for {url}: {entropy}")
        return entropy
    except:
        logger.info(f"domain_entropy for {url}: 0 (error)")
        return 0

def featureExtraction(url):
    logger.info(f"Extracting features for URL: {url}")
    features = []
    try:
        # Existing features
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
        
        # New features
        features.extend([
            subdomain_count(url),
            uses_https(url),
            has_port(url),
            special_char_count(url),
            domain_entropy(url)
        ])
        
        logger.info(f"Features extracted: {len(features)} features - {features}")
        return features
    except Exception as e:
        logger.error(f"Feature extraction failed for {url}: {e}")
        raise