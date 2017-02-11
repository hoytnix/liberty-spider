from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from lib.paths import database_path


database_url = 'sqlite:///' + database_path
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
