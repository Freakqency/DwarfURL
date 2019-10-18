from flask import Blueprint, request, render_template, redirect   
from .extensions import mongo, base62encode, Counter, red
from .settings import URI, MONGO_URI
import time 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

def insert(longurl):
    url_collection = mongo.db.url
    shorturl = base62encode(Counter())
    CreationTime = int(time.time())
    ExpirationTime = CreationTime + 86400
    if red.get(shorturl) == None:
        url_collection.insert({'LongUrl':longurl, 'ShortUrl':shorturl, 'CreationTime':CreationTime ,'ExpirationTime':ExpirationTime})
        red.set(shorturl,longurl)
        return shorturl
    else:
        return shorturl

@main.route('/<id>', methods = ['GET'])
def fetch(id):
    shorturl = id
    url = red.get(shorturl)
    if url == None:
        url_collection = mongo.db.url
        url_data = url_collection.find_one({'ShortUrl':shorturl})
        if not url_data:
            print(url_data)
            return "Invalid URL"
        return redirect(url_data['LongUrl'])
    else :
        url = url.decode('utf-8')
        return redirect(url)

@main.route('/shorten', methods = ['POST', 'GET'])
def short():
    longurl = request.form['url']
    shorturl = insert(longurl)
    shorturl = URI + shorturl
    return render_template('index.html', shorturl = shorturl)