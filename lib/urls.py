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

    if url == '':
        return False

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
        'porn', 'sex',

        # Too many sub-domains
        'tumblr.com', 'deviantart.com', 'wiki', 

        # Top 100 - should reduce DB requests
        'google', 'youtube', 'facebook', 'baidu.com', 'yahoo', 
        'wikipedia', 'qq.com', 'sohu.com', 'google.co.jp',
        'taobao.com', 'tmall.com', 'live.com', 'amazon', 'vk.com', 
        'twitter.com', 'instagram.com', '360.cn', 'linkedin.com',
        'jd.com', 'reddit.com', 'wordpress.com', 

        # Common duplicates
        'kita-kore.com','dgallery.jp','techcrunch.com','smartadserver.com',
        'spotify.com','coca-colacompany.com','cyberpatrol.com','58.com',
        'com.ni','koushunyude-hataraco.net','jugem.jp','msn.com','ikulist.me',
        'stackoverflow.com','goo.ne.jp','menshappyhellowork.com','naver.jp',
        'npr.org','blogmura.com','whoisprivacyprotect.com','female-ring.com',
        'squarespace.com','dmm.com','blogimg.jp','pocha-jiten.com',
        'patreon.com','gov.uk','hao123.com','anal-jiten.com','lti.jp',
        'force.com','mixi.jp','fuzoku-flash.jp','matomeantena.com','si.com',
        'eventbrite.com','39.net','apache.org','theatlantic.com',
        'imekura-jiten.com','chijo-jiten.com','miechat.tv','hu-ou.com',
        'girlsheaven-job.net','exe-web.com','519.jp','fubaito.jp','youku.com',
        'com.hn','deliichi.jp','fz-5.com','privacymark.jp','sitemeter.com',
        'asacp.org','netnanny.com','bloomberg.com','constantcontact.com',
        'nifty.com','momojob.net','valuecommerce.com','eyes.tv','night-life.jp',
        'hotel-deli.com','tgbus.com','bbc.co.uk','manzoku.or.jp',
        'moudamepo.com','atarijo.com','anquan.org','tokyo-fuu.com',
        'zokuzoku.jp','inc-connect.jp','usatoday.com','ganji.com','dmm.co.jp',
        'go.com','fuzokubijin.com','fuuzoku.info','co.cr','com.bo',
        'taiken-nyuten.net','huffingtonpost.com','amzn.to','delikun.com',
        'funv.jp','omniture.com','forbes.com','paypal.com','hugedomains.com',
        'legacy.com','issuu.com','from-f.net','coca-cola.com','a-base.net',
        'fuzokustyle.jp','happyhellowork.com','reuters.com','delinote.jp',
        '2ch-c.net','com.gt','truste.com','eroterest.net','doubleclick.net',
        'github.io','bee-net.co.jp','seesaa.net','deli-spot.net','naitopi.com',
        'message','mens-v.com','ticketmaster.com','epoch.com','nicovideo.jp',
        'fansided.com','ac.uk','ninja.co.jp','python.org','eepurl.com',
        'sedoparking.com','jukujo-jiten.com','dtiblog.com','ranking-deli.jp',
        'addtoany.com','f-terminal.jp','ifeng.com','cnn.com','com.py',
        'theguardian.com','with2.net','fuzokuou.com','a-fuu.com','elog-ch.net',
        'slideshare.net','sidearmsports.com','51.la','delicon.jp','com.pe',
        'yorutobi.net','fuzoku-navi.tv','snapchat.com','olark.com','com.ve',
        'fuzoku24.com','fuzokunv.com','mozilla.org','ldblog.jp','2chblog.jp',
        'addthis.com','bbb.org','dpress.jp','girl-jiten.com','fuzoku-move.net',
        'kir.jp','a-deli.jp','purelovers.com','sedo.com','wsj.com',
        'dtiserv2.com','deri-ou.com','fuuzoku-tv.com','zendesk.com',
        'fuzoku-watch.com','djnl.jp','king-fuzoku.com','qzin.jp','163.com',
        'dh-jiten.com','rakuten.co.jp','fucolle.com','typepad.com','xrea.com',
        'soundcloud.com','sakura.ne.jp','melon-jiten.com','deli-fuzoku.jp',
        'f-douga.com','com.uy','blogger.com','washingtonpost.com',
        'rtalabel.org','livedoor.biz','45to.jp','a8.net','ccbill.com',
        'fzk.ne.jp','fuzoku-station.net','fuzoku-info.com','feedly.com',
        'asageifuzoku.com','medium.com','sina.com.cn','apserver.net',
        'livedoor.com','xing.com','dl-city.net','w3.org','shinobi.jp',
        'ameblo.jp','i2i.jp','statcounter.com','fuzoku.jp','co.za',
        'cityheaven.net','miitbeian.gov.cn','blog.jp','line.me',
        'deriheru-1m.com','beian.gov.cn','miibeian.gov.cn','nytimes.com',
        'youtu.be','fujoho.jp','dto.jp','goo.gl','creativecommons.org','bit.ly',
        'adobe.com','microsoft.com','doorblog.jp','feedburner.com','weibo.com',
        'vimeo.com','t.co','livedoor.jp','hatena.ne.jp','blogspot.com',
        'flickr.com','ziyu.net','github.com','wordpress.org','fc2.com',
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

    return url


def same_origin(a, b):
    return urlparse(sanitize_url(a)).netloc == urlparse(sanitize_url(b)).netloc


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