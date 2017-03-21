from pprint import PrettyPrinter
from concurrent.futures import ProcessPoolExecutor
from asyncio import Queue

from lycosidae.database import redis_sites, redis_techs
# Config
from lycosidae.settings import SETTINGS
from lycosidae.log import logger
# Functions
from lycosidae.tasks.crawl import Scraper
from lycosidae.tasks.profile import Profiler
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
                        pass
                        #_ = None
            else:
                self.worker()

            if redis_sites.size >= SETTINGS['ENGINE_QUEUE_SIZE']:
                # Process Redis-Sites
                result_queue = []
                for key in redis_sites.keys:
                    print(key)

                    results = redis_sites.get(key).split(',')[:-1]

                    print(results)

                    for result in results:
                        result_queue.append(result)
                result_queue = set(result_queue)

                site_queue = []
                with ProcessPoolExecutor(max_workers=SETTINGS['ENGINE_CONCURRENCY'] or 1) as e:
                    for uniqueness, url in zip(result_queue, e.map(Site.is_unique, result_queue)):
                        if uniqueness:
                            site_queue.append(url)
                Site.bulk_insert(urls=site_queue)

                redis_sites.flushdb()

            if redis_techs.size >= SETTINGS['ENGINE_QUEUE_SIZE']:
                # Process Redis-Techs
                for key in redis_techs.keys:
                    results = redis_techs.get(key).split(',')[:-1]
                    s = Site.select({'url': key})
                    s.update_profile(results)

            # Graceful shutdown.
            with open(exit_path, 'r') as stream:
                if 'quit' in stream.read().strip().lower():
                    break

    def worker(self, process=None):
        while True:
            # Graceful shutdown.
            if redis_sites.size >= SETTINGS['ENGINE_QUEUE_SIZE']:
                break

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
            profile = Profiler(html=html)
            o = [key for key in profile.d if profile.d[key]]
            redis_techs.db.sadd(site.url, o)

            # Scraper
            scraper = Scraper(site=site.url, html=html)
            redis_sites.db.sadd(site.url, scraper.results)

            # Log
            log_str = '[{}] {}'.format(process, site.url)
            print(log_str)