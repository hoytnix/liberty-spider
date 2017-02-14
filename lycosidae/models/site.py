import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, \
    inspect

from lib.urls import sanitize_url
from lycosidae.database import Base, session
from lycosidae.settings import SETTINGS


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)

    url = Column(String)
    wordpress = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=None)

    def update_profile(self, profile):
        self.wordpress = profile
        session.merge(self)
        session.commit()     

    def update_last_checked(self):
        self.last_checked = datetime.datetime.utcnow()
        session.merge(self)
        session.commit()

    @classmethod
    def queue(self):
        return session.query(Site).filter_by(last_checked=None) \
                                  .order_by(Site.id) \
                                  .limit(SETTINGS['ENGINE_QUEUE_SIZE'])
                                  
    @classmethod
    def queue_next(self):
        from random import random

        table = session.query(Site)
        row_count = int(table.count())

        s = None
        while True:
            s = ( session.query(Site).filter_by(last_checked=None)
                    # should eliminate duplicate requests
                    .offset(
                        random() * row_count
                    )
                    .limit(1)
                    .first()
                )
            if s is not None:
                break

        s.update_last_checked()
        return s