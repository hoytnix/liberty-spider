import logging
from datetime import datetime
from random import random

from sqlalchemy import Column, Integer, Boolean, DateTime, Text, String, func, exc
from sqlalchemy.sql import exists

from lycosidae.database import Base, session
from lib.urls import schemeless


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)

    url = Column(Text)
    wordpress = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=None)

    def update_profile(self, profile):
        #count = 0
        #while True:
        #    try:
        self.wordpress = profile
        session.merge(self)
        session.commit()
        #        return
        #    except sqlalchemy.exc.OperationalError:
        #        count += 1
        #        if count > 3:
        #            print('[CRITICAL] Loss of data!')
        return

    def update(self):
        self.last_checked = datetime.utcnow()
        session.merge(self)
        session.commit()
        
    @classmethod
    def next(cls):
        table = session.query(Site)
        row_count = int(table.count())

        count = 0
        s = None
        while True:
            s = ( session.query(Site).filter_by(last_checked=None)
                    # should eliminate duplicate requests
                    .offset(
                        int(row_count * random())
                    )
                    .limit(1)
                    .first()
                )
            if s is not None:
                break
            count += 1
            if count > 3:
                return

        s.update()
        return s

    @classmethod
    def insert(cls, url):
        #count = 0
        #while True:
        #    try:

        # Sanatize.
        url = schemeless(url)

        if not session.query(exists().where(Site.url == url)).scalar():
            new_site = Site(url=url)
            session.add(new_site)
            session.commit()
        else:
            logging.info('DUPLICATE ' + url)
            session.rollback()

        #        return
        #    except sqlalchemy.exc.OperationalError:
        #        count += 1
        #        if count > 3:
        #            print('[CRITICAL] Loss of data!')
        return

    @classmethod
    def bulk_insert(cls, urls):
        session.bulk_save_objects([Site(url=url) for url in urls])
        session.commit()

    @classmethod
    def is_unique(cls, url):
        return session.query(exists().where(Site.url == url)).scalar()