import re
from urllib.parse import urlparse
import arabic_reshaper
from bidi.algorithm import get_display

def rtl(text):
    text = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', str(text))
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def is_valid_url(url: str) -> bool:
    try:
        u = urlparse(url)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except:
        return False
