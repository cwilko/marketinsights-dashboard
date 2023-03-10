import redis
from redis_cache import RedisCache
from json import JSONEncoder, dumps

import pickle
import pandas as pd


def serialize(data):
    return pa.serialize(data).to_buffer().to_pybytes()


def deserialize(data):
    return pa.deserialize(data)

client = redis.Redis(host='192.168.1.205', port=6379, db=0)
cache = RedisCache(redis_client=client, serializer=pickle.dumps, deserializer=pickle.loads)


@cache.cache()
def test(x):
    print("CALLED")
    return pd.DataFrame({"A": [1, 2, 3]})

test.invalidate_all()
print(test(2))
