from pprint import PrettyPrinter
from concurrent.futures import ProcessPoolExecutor

# Config
from lycosidae.settings import SETTINGS
# Functions
from lycosidae.wordpress import WordPress
from lycosidae.scraper import Scraper
# Models
from lycosidae.models.site import Site
# Library
from lib.http import download
from lib.paths import exit_path


class Lycosidae:
    def __init__(self):
        PrettyPrinter(indent=4).pprint(SETTINGS)

        # Create new exit-flag file.
        with open(exit_path, 'w+') as stream:
            pass

        while True:
            # Collect results.
            if SETTINGS['ENGINE_CONCURRENCY'] > 0:
                with ProcessPoolExecutor(max_workers=SETTINGS['ENGINE_CONCURRENCY']) as e:
                    for _ in e.map(self.worker, range(SETTINGS['ENGINE_CONCURRENCY'])):
                        _ = None
            else:
                self.worker()

            # Graceful shutdown.
            with open(exit_path, 'r') as stream:
                if 'quit' in stream.read().strip().lower():
                    break

    def worker(self, process=None):
        while True:
            # Graceful shutdown.
            with open(exit_path, 'r') as stream:
                if 'quit' in stream.read().strip().lower():
                    break

            # ----- Work -----

            site = Site.next()
            if not site:
                continue

            html = download(site.url)
            if not html:
                continue # TODO: update the db with the result

            # Profiler
            wordpress = WordPress(url=site.url, html=html)
            profile = wordpress.is_wordpress
            site.update_profile(profile)

            # Scraper
            scraper = Scraper(site=site.url, html=html)
            for result in scraper.results:
                Site.insert(url=result)

            # Log
            log_str = '[{}] {}'.format(process, site.url)
            print(log_str)