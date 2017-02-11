from bs4 import BeautifulSoup
from urllib.parse import urljoin

from lib.http import download


class WordPress:
    def __init__(self, url, html=None):
        self.is_wordpress = False
        if not html:
            html = download(url)

        """ Homepage HTML -->
                Let's try not to hit up too many pages. :)
        """

        # First check the footer.
        if 'proudly powered by wordpress' in html.lower():
            self.is_wordpress = True
            return

        # Check source for wp-content folders
        soup = BeautifulSoup(html, 'html.parser')
        links = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
        for link in links:
            if 'wp-content' in link:
                is_wordpress = True
                return

        """ Page requests -->
                These require downloading more pages.
        """

        # Safe: try for the license.txt
        page = urljoin(url, 'license.txt')
        html = download(page)
        if html:
            if 'WordPress' in html:
                self.is_wordpress = True
                return

        # Lastly, try to hit up the login page.
        if False: # TODO: should be configurable from config file
            page = urljoin(url, 'wp-login.php')
            if download(page): #shouldn't be 404
                self.is_wordpress = True
                return