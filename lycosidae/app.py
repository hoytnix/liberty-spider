import time
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.sql import exists

from lycosidae.settings import SETTINGS
from lycosidae.database import session
from lycosidae.models.site import Site
from lycosidae.wordpress import WordPress
from lycosidae.scraper import Scraper

from lib.http import download


def loop():
    while True:
        start_time = time.time()

        loop_results = []
        sites = Site.queue()
        with ProcessPoolExecutor(max_workers=SETTINGS['ENGINE_CONCURRENCY'] * 2) as e:
            for (site, profile, scraping) in e.map(work, sites):
                loop_results.append((site, profile, scraping))

        new_site_count = 0
        for loop_result in loop_results:
            site, profile, scraping = loop_result

            print('UPDATE: {} {}'.format(site.url, profile))
            if profile:
                site.update_profile(profile)
            site.update_last_checked()
            
            for result in scraping:
                if not session.query(exists().where(Site.url == result)).scalar():
                    new_site = Site(url=result)
                    session.add(new_site)
            new_site_count += scraping.__len__()
        session.commit()

        total_time = time.time() - start_time
        print(new_site_count, total_time)


def work(site):
    html = download(site.url)
    if not html:
        return [site, None, []]

    # Profiler
    wordpress = WordPress(url=site.url, html=html)
    profile = wordpress.is_wordpress

    # Scraper
    s = Scraper(site=site.url, html=html)
    scraping = s.results

    return site, profile, scraping
