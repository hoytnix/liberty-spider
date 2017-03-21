import logging
from datetime import datetime
from random import random

from sqlalchemy import Table, Column, Integer, Boolean, DateTime, Text, String, func, exc
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from lycosidae.database import Base, session
from lycosidae.models.technology import Technology
from lib.urls import schemeless

site_technologies = Table('site_technologies', Base.metadata,
    Column('site_id', Integer, ForeignKey('sites.id')),
    Column('technology_id', Integer, ForeignKey('technologies.id'))
)


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)

    # Relationships
    technologies = relationship("Technology", secondary=site_technologies)

    # Details
    url = Column(Text)
    last_checked = Column(DateTime, default=None)

    def update_profile(self, profile):
        #count = 0
        #while True:
        #    try:
        for technology in profile:
            t = Technology.select_or_insert(title=technology)
            self.technologies.append(t)

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
            #logging.info('DUPLICATE ' + url)
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
        does_exist = session.query(exists().where(Site.url == url)).scalar()
        return not does_exist

    @classmethod
    def select(cls, kv):
        return session.query(Site).filter_by(**kv).first() # TODO: should be one