from flask import Blueprint, render_template, request, redirect
from .extensions import  *
from .settings import URI

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/shorten', methods = ['POST', 'GET'])
def shorten():
    long_url = request.form['url']        
    short_url = fetch_short_url(long_url)
    if (short_url == None):        
        seed = fetch_seed()
        short_url = encode_url(seed)
        url_insert(long_url, short_url)
        cache_insert(short_url, long_url)
    short_url = URI + short_url
    return render_template('index.html', shorturl = short_url)

@main.route('/<short_url>', methods = ['GET'])
def map_url(short_url: str):
    long_url = cache_fetch(str(short_url))
    if (long_url == None):
        long_url = fetch_long_url(short_url)    
    long_url = fetch_long_url(short_url)
    return redirect(long_url)