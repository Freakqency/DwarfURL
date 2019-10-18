from flask_pymongo import PyMongo 
from .settings import REDIS_URL
import redis

mongo = PyMongo()
red = redis.from_url(REDIS_URL)

#My Base62 Implementation
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62encode(seed):
    if seed == 0:
        return BASE62[0]
    res=[]
    while seed:
        seed, rem = divmod(seed,len(BASE62))
        res.append(BASE62[rem])
    res.reverse()
    return "".join(res)

#Static Counter Implementation
count = 99999999999 #XXX:To be assigned using zookeeper
def Counter():  
 global count  
 count = count + 1  
 return count  
    