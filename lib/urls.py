from urllib.parse import urlparse, urljoin, urlunsplit


def sanitize_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    if url.startswith('//'):
        return 'http:' + url
    
    return 'http://' + url


def sanitize_links(origin, destination):
    # Is it an unsupported scheme?
    blacklist = ['mailto:', 'ftp:']
    for scheme in blacklist:
        if destination.startswith(scheme):
            return False

    # If its already an absolute url, do nothing.
    if destination.startswith('http://') or destination.startswith('https://'):
        return destination

    # Is it a fragment?
    if destination[0] == '#':
        return urljoin(origin, destination)

    # Is it a relative path?
    if destination[0] == '/':
        return urljoin(origin, destination)


def same_origin(a, b):
    oa = urlparse(a)
    ob = urlparse(b)
    return oa.netloc == ob.netloc


def domain_only(url):
    o = urlparse(url)
    return urlunsplit((o.scheme, o.netloc, '', '', ''))