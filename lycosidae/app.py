from threading import Thread
from queue import Queue

from lycosidae.database import session
from lycosidae.models.site import Site
from lycosidae.wordpress import WordPress
from lycosidae.scraper import Scraper


class Lycosidae:
    def __init__(self):
        e_site = Site(url='https://blog.todoist.com/')
        #session.add(e_site)
        #session.commit()
        self.work(e_site)
        return

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

    def work(self, site):
        #while True:
        #site = self.q.get()

        wordpress = WordPress(url=site.url)
        site.wordpress = wordpress.is_wordpress

        s = Scraper(site=site.url)

        print('\n', s.results.__len__(), '\n')
        for result in s.results:
            print(result)
        # for link in links:
        #   site = ...

        # site.last_checked = time()

        #self.q.task_done()
        return