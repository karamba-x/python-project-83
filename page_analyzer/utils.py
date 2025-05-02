from urllib.parse import urlparse


def parse_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"