from urllib.parse import urlparse


def sanitize_url(url, comparison=None):
    oo = urlparse(url)
    if not comparison:
        if oo.scheme:
            return url
        else:
            return 'http://' + url

    od = urlparse(comparison)

    # Do both urls have a scheme?
    if oo.scheme and od.scheme:
        # Then there's nothing left to do!
        return url

    # Otherwise, do they have the same netloc?
    if oo.netloc == od.netloc:
        # The destination is a relative url.
        return 'http://' + url

    # The destination probably just lacks a scheme.
    return 'http://' + url


def same_origin(a, b):
    oa = urlparse(a)
    ob = urlparse(b)
    return oa.netloc == ob.netloc