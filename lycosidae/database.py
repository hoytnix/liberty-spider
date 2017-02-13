from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from lib.paths import database_path

database_url = 'sqlite:///' + database_path

engine = create_engine(database_url, echo=False, poolclass=NullPool)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
