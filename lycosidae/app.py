from threading import Thread
from queue import Queue

from sqlalchemy.sql import exists

from lycosidae.database import session
from lycosidae.models.site import Site
from lycosidae.wordpress import WordPress
from lycosidae.scraper import Scraper


class Lycosidae:
    def __init__(self):
        new_site = Site(url='http://hoyt.io')
        session.add(new_site)
        session.commit()

        self.work(new_site)

        '''
        concurrency = 2
        self.q = Queue(concurrency * 2)
        for i in range(concurrency):
            t = Thread(target=self.work)
            t.daemon = True
            t.start()

        while True:
            for site in Site.queue:
                self.q.put(site)
            self.q.join()
        '''
        return

    def work(self, site):
        #while True:
        #site = self.q.get()

        wordpress = WordPress(url=site.url)
        site.wordpress = wordpress.is_wordpress

        s = Scraper(site=site.url)
        for result in s.results:
            if not session.query(exists().where(Site.url == result)).scalar():
                new_site = Site(url=result)
                session.add(new_site)
        print(session.new)

        # for link in links:
        #   site = ...

        # site.last_checked = time()

        #self.q.task_done()
        return