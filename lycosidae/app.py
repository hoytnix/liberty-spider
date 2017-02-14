import pprint
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.sql import exists

from lycosidae.settings import SETTINGS
from lycosidae.database import session
from lycosidae.models.site import Site
from lycosidae.wordpress import WordPress
from lycosidae.scraper import Scraper

from lib.http import download
from lib.paths import exit_path


class Lycosidae:
    def __init__(self):
        #worker()
        #return

        pprint.PrettyPrinter(indent=4).pprint(SETTINGS)

        # Create new exit-flag file.
        with open(exit_path, 'w+') as stream:
            pass
        self.do_work = True

        with ProcessPoolExecutor(max_workers=SETTINGS['ENGINE_CONCURRENCY']) as e:
            for _ in e.map(self.worker, range(SETTINGS['ENGINE_CONCURRENCY'])):
                _ = None


    def worker(self, process=None):
        while True:
            site = Site.queue_next()
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
                if not session.query(exists().where(Site.url == result)).scalar():
                    new_site = Site(url=result)
                    session.add(new_site)
                    session.commit()

            log_str = '[{}] {}'.format(process, site.url)
            print(log_str)

            # Graceful shutdown.
            with open(exit_path, 'r') as stream:
                if stream.read().strip().lower() == 'quit':
                    self.do_work = False

            if not self.do_work:
                break