def get_http_version_of_url(url):
    if url.startswith("https://"):
        return "http" + url[5:]
    else:
        return url
