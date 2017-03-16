from sqlalchemy import Column, Integer, Text
from sqlalchemy.sql import exists

from lycosidae.database import Base, session


class Technology(Base):
    __tablename__ = 'technologies'
    id = Column(Integer, primary_key=True)

    title = Column(Text)

    @classmethod
    def select_or_insert(cls, title):
        if not session.query(exists().where(Technology.title == title)).scalar():
            t = Technology(title=title)
            session.add(t)
            session.commit()

            return t
        return session.query(Technology).filter_by(title=title).first()
