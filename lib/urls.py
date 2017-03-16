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

    # ----- Filter -----

    o_url = url
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

    # Blacklisted domains
    blacklist = SETTINGS['URL_TLD_BLACKLIST']
    for o in blacklist:
        if url.endswith(o):
            return False

    # Blacklisted websites
    blacklist = [
        # ...
        'porn', 'sex', 'hentai', 'adult', 'xxx', 'gay', 'nude', 'teen', 'ero',
        'ebony', 'escort', 'dick',

        # Too many sub-domains
        'tumblr.com', 'deviantart.com', 'wiki', 

        # Top 100 - should reduce DB requests
        'google', 'youtube', 'facebook', 'baidu.com', 'yahoo', 
        'wikipedia', 'qq.com', 'sohu.com', 'google.co.jp',
        'taobao.com', 'tmall.com', 'live.com', 'amazon', 'vk.com', 
        'twitter.com', 'instagram.com', '360.cn', 'linkedin.com',
        'jd.com', 'reddit.com', 'wordpress.com', 
    ]
    for o in blacklist:
        if o in url:
            return False

    # ----- Validate -----

    # Is it valid?
    try:
        u = urlparse(url)
    except ValueError as e:
        # Invalid IPv6 URL
        return False 

    tld = None
    if not u.scheme:
        # Let's see if it has a domain.
        path = u.path
        path = path.split('/')[0]
        tld = tld_of(path)

        # Cool, just add a scheme.
        if tld:
            url = 'http://' + url
        else: # It must be relative.
            url = urljoin(origin, url)
    if not tld:
        tld = tld_of(u.netloc)

    # Subdomain options
    if not SETTINGS['HTTP_SUBDOMAINS_ENABLED']:
        if tld:
            u = urlparse(url)
            o = u.netloc.replace(tld, '').split('.')
            if o.__len__() > 1: # There is atleast one dubdomain.
                url = u._replace(netloc=o[-1] + tld).geturl()

    #if url == '':
    #    return False

    for c in '0123456789':
        if c in url:
            return False

    return url


def same_origin(destination, origin):
    for fragment in '/?#':
        if destination.startswith(fragment):
            return True

    return urlparse(sanitize_url(destination)).netloc == urlparse(sanitize_url(origin)).netloc


def domain_only(url):
    u = urlparse(sanitize_url(url))
    return urlunparse( (u.scheme, u.netloc, '', '', '', '') )


def tld_of(url):
    """Right now it only accepts urls with no slashes."""

    two_levels = []
    one_level = []
    for extension in all_tlds():
        if extension.split('.').__len__() == 2:
            two_levels.append('.' + extension)
        else:
            one_level.append('.' + extension)

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

    return domain_tld or False


def schemeless(url):
    return urlparse(url)._replace(scheme='').geturl()[2:]


class URL:
    def __init__(self, location, origin=None):
        """
            TODO:
            - [ ] TLD Blacklist
            - [ ] Number blacklist
            - [ ] IP blacklist
        """

        self.fqu = None

        # Above all else, normalize it.
        location = location.lower()

        # Secondly, filter out keywords we don't want.
        if keyword_blacklist(url=location):
            return

        # Catch invalid IPv6 URLs
        try:
            u = urlparse(location)
        except ValueError as e:
            return

        self.tld = None
        if not u.scheme:
            path = u.path.split('/')[0]
            


    def keyword_blacklist(self, url):
        cwd = path.dirname(path.abspath(__file__))
        _dir = path.join(cwd, 'blacklist')

        x = []
        for (root, _, file_names) in walk(_dir):
            for file_name in file_names:
                fp = path.join(root, file_name)
                with open(fp, 'r') as stream:
                    for line in stream:
                        l = line.strip()
                        if l != '' and not l.startswith('#'):
                            x.append(l)

        for o in x:
            if o in url:
                return True        