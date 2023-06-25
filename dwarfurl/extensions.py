from flask_pymongo import PyMongo
import redis
from random import randrange
from .settings import REDIS_URI, REDIS_PASSWORD

red = redis.Redis(host=REDIS_URI,
                 port=12688,
                 password=REDIS_PASSWORD)
mongo = PyMongo()

def encode_url(seed: int)-> str:
    '''
    Function to encode url using base62
    :param - seed(int): random integer seed
    :return - short_url(str): generated short url
    '''
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if seed == 0:
        return CHAR[0]
    res = []
    while seed:
        seed, rem = divmod(seed, len(CHAR))
        res.append(CHAR[rem])
    res.reverse()
    return "".join(res)

def insert_seed(new_seed: int)-> None:
    '''
    Function to insert the generated seed
    :param - new_seed(int): random integer seed
    '''
    counter_collection = mongo.db.counter
    record = {'seed': new_seed}
    counter_collection.insert_one(record)

def fetch_seed()-> int:
    '''
    Function to generate radom seed in given range
    :return seed(int) - generate random integer seed
    '''
    seed = randrange(9999999)
    while mongo.db.counter.find_one({'seed': seed}):
        seed = randrange(9999999)
    insert_seed(seed)
    return seed

def url_insert(long_url: str, short_url: str)-> None:
    '''
    Function to insert long_url:short_url mapping into the DB
    :param - long_url(str) - given long URL
    :param - short_url(str) - generated short URL
    '''
    url_collection = mongo.db.url
    record = { "long_url" : long_url, "short_url" : short_url }
    url_collection.insert_one(record)

def fetch_long_url(short_url)-> str:
    '''
    Function to fetch long URL for given short URL
    :param - short_url(str): given short URL
    :return long_url(str): fetched long URL
    '''
    url_collection = mongo.db.url.find_one({ "short_url" : short_url}, { 'long_url' : True})
    if (url_collection == None):
        return None
    long_url = url_collection['long_url']
    return long_url

def fetch_short_url(long_url: str)-> str:
    '''
    Function to fetch short URL from DB if it exists
    :param - long_url(str): given long URL
    :return - short_url(str): fetched short URL
    '''
    url_collection = mongo.db.url.find_one({ "long_url" : long_url }, { 'short_url' : True })
    if (url_collection == None):
        return None
    short_url = url_collection['short_url']
    return short_url

def cache_insert(short_url: str, long_url: str)-> None:
    '''
    Function to store {short_url:long_url} mapping in redis
    :param short_url(str): generated short URL:
    :param long_url(str): given long URL
    '''
    red.set(short_url, long_url)

def cache_fetch(short_url)-> str:
    '''
    Function to fetch long URL for given short_url
    :param short_url(str): generated short_url
    :return long_url(str): fetched long_url
    '''
    return red.get(short_url)