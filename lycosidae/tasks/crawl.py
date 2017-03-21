from bs4 import BeautifulSoup

from lycosidae.settings import SETTINGS
from lycosidae.log import logger

from lib.http import download
#from lib.urls import sanitize_url, same_origin, domain_only, URL
from lib._urls import URL


class Scraper:
    def __init__(self, site, html=None):
        # Level 0
        inbound, outbound = self.links_from_page(site, html=html)

        current_depth = inbound
        for depth in range(SETTINGS['SCRAPER_SEARCH_DEPTH']):
            next_depth = []
            for link in current_depth:
                o_inbound, o_outbound = self.links_from_page(link)
                for new_link in o_inbound:
                    next_depth.append(new_link)
                for new_link in o_outbound:
                    outbound.append(new_link)
            current_depth = next_depth

        self.results = set(outbound)

    def links_from_page(self, site, html=None):
        if not html:
            html = download(site)
            if not html:
                return [], [] # the page did not download!

        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            if link.get('href'):
                links.append(link.get('href'))

        inbound = []
        outbound = []
        for link in links:
            u = URL(link)

            if not u.domain:
                continue

            if site == u.domain:
                inbound.append(u.fqu)
            else:
                outbound.append(u.domain)

        return [x for x in set(inbound)], [x for x in set(outbound)]
