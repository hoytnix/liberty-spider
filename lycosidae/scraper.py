from bs4 import BeautifulSoup

from lib.http import download
from lib.urls import sanitize_links, same_origin, domain_only


class Scraper:
    def __init__(self, site, html=None):
        # Level 0
        inbound, outbound = self.links_from_page(site, html=html)

        current_depth = inbound
        for depth in range(1):
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

        soup = BeautifulSoup(html, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

        inbound = []
        outbound = []
        for link in links:
            link = sanitize_links(origin=site, destination=link)

            if same_origin(link, site):
               inbound.append(link)
            else:
               outbound.append(domain_only(link))

        return [x for x in set(inbound)], [x for x in set(outbound)]