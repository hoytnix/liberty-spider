import redis


class RedisDB:
    def __init__(self, host, port, db, password):
        self.db = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def append(self, key, value):
        self.db.append(key=key, value=value)

    def get(self, key):
        return self.db.get(key).decode('utf-8')

    def flushdb(self):
        self.db.flushdb()

    @property
    def size(self):
        return self.db.dbsize()

    @property
    def keys(self):
        return [k for k in self.db.scan(cursor=0)[1]]