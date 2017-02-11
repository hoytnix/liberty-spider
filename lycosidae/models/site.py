from sqlalchemy import Column, Integer, String, Boolean, DateTime

from lib.urls import sanitize_url
from lycosidae.database import Base, session


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)

    url = Column(String)
    wordpress = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=None)

    @property
    def queue(self):
        return Site.query.filter(Site.wordpress == False) \
                         .filter(Site.last_checked != None)\
                         .limit(10)

    def __init__(self, url, wordpress=None, last_checked=None):
        self.url = url
