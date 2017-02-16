from bs4 import BeautifulSoup

from lycosidae.settings import SETTINGS

from lib.http import download
from lib.urls import sanitize_url, same_origin, domain_only


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
            original_link = link + ''
            link = sanitize_url(link, origin=site)

            #if link:
            #    download(link, original_url=original_link)
            
            if not link:
                continue

            if same_origin(link, site):
                inbound.append(link)
            else:
                outbound.append(domain_only(link))

        return [x for x in set(inbound)], [x for x in set(outbound)]
