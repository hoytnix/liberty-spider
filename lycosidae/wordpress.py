from bs4 import BeautifulSoup
from urllib.parse import urljoin

from lib.http import download


class WordPress:
    def __init__(self, url, html=None):
        self.is_wordpress = False
        if not html:
            html = download(url).lower()
        """ Homepage HTML -->
                Let's try not to hit up too many pages. :)
        """

        # TODO: Clean this code up...
        keys = ['wp-content', 'wp-includes', 'wp-admin']
        for key in keys:
            if key in html:
                self.is_wordpress = True
                return
        return

        # First check the footer.
        if 'proudly powered by wordpress' in html.lower():
            self.is_wordpress = True
            return

        # Check source for wp-content folders
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.findAll('link'):
            try:
                if 'stylesheet' in link.get('rel'):
                    if 'wp-content' in link.get('href'):
                        self.is_wordpress = True
                        return
            except:
                continue
        
        """ Page requests -->
                These require downloading more pages.
        """

        # Safe: try for the license.txt
        if False: # TODO: should be configurable from config file
            page = urljoin(url, 'license.txt')
            html = download(page)
            if html:
                if 'WordPress' in html:
                    self.is_wordpress = True
                    return

        # Lastly, try to hit up the login page.
        if False:  # TODO: should be configurable from config file
            page = urljoin(url, 'wp-login.php')
            if download(page):  #shouldn't be 404
                self.is_wordpress = True
                return
