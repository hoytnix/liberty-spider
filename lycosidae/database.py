from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from lib.redis_db import RedisDB
from lycosidae.settings import SETTINGS

""" MySQL Database """

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


""" Redis Database """

redis_sites = ( RedisDB(
    host=SETTINGS['REDIS_SITES_HOST'],
    port=SETTINGS['REDIS_SITES_PORT'],
    db=SETTINGS['REDIS_SITES_DB'],
    password=SETTINGS['REDIS_SITES_PASS']
))

redis_techs = ( RedisDB(
    host=SETTINGS['REDIS_TECHS_HOST'],
    port=SETTINGS['REDIS_TECHS_PORT'],
    db=SETTINGS['REDIS_TECHS_DB'],
    password=SETTINGS['REDIS_TECHS_PASS']
))
