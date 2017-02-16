from os import path, walk
from urllib.parse import urlparse, urljoin, urlunparse

from lycosidae.settings import SETTINGS


def all_tlds():
    cwd = path.dirname(path.abspath(__file__))
    _dir = path.join(cwd, 'tlds')

    x = []
    for (root, _, file_names) in walk(_dir):
        for file_name in file_names:
            fp = path.join(root, file_name)
            with open(fp, 'r') as stream:
                for line in stream:
                    x.append(line.strip())
    return set(x)


def sanitize_url(url, origin=False):
    """Marshals all URLs to be compatible with the database.
    
    If it returns False then skip it.
    """

    url = url.lower()

    # Irrelevant schemes
    blacklist = [
        'mailto:', 'ftp:', 'irc:', 'javascript:', 'tel:', 'rtmp:', 'rtsp:',
        'webcal:', 'itpc:', 'line:', 'zune:', 'skype:', 'gtalk:', 'feed:',
        'whatsapp:'
    ]
    for scheme in blacklist:
        if url.startswith(scheme):
            return False

    # Is it valid?
    u = urlparse(url)
    if not u.scheme:
        # Let's see if it has a domain.
        path = u.path
        path = path.split('/')[0]

        two_levels = []
        one_level = []
        for extension in all_tlds():
            if extension.split('.').__len__() == 2:
                two_levels.append('.' + extension)
            else:
                one_level.append('.' + extension)

        domain_tld = None
        for extension in two_levels:
            if path.endswith(extension):
                domain_tld = extension
                break

        if not domain_tld:
            for extension in one_level:
                if path.endswith(extension):
                    domain_tld = extension
                    break

        # Cool, just add a scheme.
        if domain_tld:
            return 'http://' + url
        else: # It must be relative.
            return urljoin(origin, url)

    return url


    # Fragment
    if url.startswith('#'):
        return False

    # Relative scheme
    if url.startswith('//'):
        url = 'http:' + url

    # Relative link
    if url.startswith('/') or url.startswith('?'):
        return False

    # Irrelevant schemes
    blacklist = [
        'mailto:', 'ftp:', 'irc:', 'javascript:', 'tel:', 'rtmp:', 'rtsp:',
        'webcal:', 'itpc:', 'line:', 'zune:', 'skype:', 'gtalk:', 'feed:',
        'whatsapp:'
    ]
    for scheme in blacklist:
        if url.startswith(scheme):
            return False

    # Remember the scheme
    scheme = url.split('//')[0] + '//'
    url = url.replace(scheme, '')

    # Remove the path
    url = url.split('/')[0]

    # Figure out the tld
    two_levels = []
    one_level = []
    for extension in all_tlds():
        if extension.split('.').__len__() == 2:
            two_levels.append(extension)
        else:
            one_level.append(extension)
    
    domain_tld = None
    for extension in two_levels:
        if url.endswith(extension):
            domain_tld = extension
            break

    if not domain_tld:
        for extension in one_level:
            if url.endswith(extension):
                domain_tld = extension
                break

    if not domain_tld:
        return False
    else:
        domain_tld = '.' + domain_tld

    # Is the tld blacklisted?
    for blacklist in SETTINGS['URL_TLD_BLACKLIST']:
        if blacklist in domain_tld:
            return False

    # Strip everything!
    url = url.replace(domain_tld, '')
    domain_name = url.split('.')[-1]

    return scheme + domain_name + domain_tld


def same_origin(a, b):
    return urlparse(sanitize_url(a)).netloc == urlparse(sanitize_url(b)).netloc


def domain_only(url):
    u = urlparse(sanitize_url(url))
    return urlunparse( (u.scheme, u.netloc, '', '', '', '') )