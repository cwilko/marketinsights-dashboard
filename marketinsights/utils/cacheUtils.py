import redis
import pickle
from redis_cache import RedisCache

client = redis.Redis(host='192.168.1.205', port=6379, db=0)
redis_cache = RedisCache(redis_client=client, serializer=pickle.dumps, deserializer=pickle.loads)


def cache():
    return redis_cache.cache()
