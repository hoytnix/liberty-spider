from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from lycosidae.settings import SETTINGS

database_url = 'mysql+pymysql://{user}:{_pwd}@{host}/{name}?charset=utf8mb4'.format(
    user=SETTINGS['DATABASE_USER'],
    _pwd=SETTINGS['DATABASE_PASS'],
    host=SETTINGS['DATABASE_HOST'],
    name=SETTINGS['DATABASE_NAME']
)

engine = create_engine(database_url, echo=False, poolclass=NullPool)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
