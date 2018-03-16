from urllib.request import Request, urlopen
from multiprocessing.pool import ThreadPool
import json
import re

## you need to install this python 3.x library
import tweepy

#nasty regex for grabbing the urls
PATTERN = '''<a\sclass=\"twitter-timeline\" href=\"(.*)\" data-widget'''
p = re.compile(PATTERN, re.IGNORECASE)

##############################################
consumer_key = 't4oEoD2LWV7Kc66t14kAlmbAG'
consumer_secret = 'LEdr1dKJYjpNEPyFP7B4wAs7uZboCJ77DcCVnkTOrNXypxC5j1'
access_token = '2763184212-kHsrhWWKWP6kN5SVMXD6ZJ09HdSJUZx4QSuFqdR'
access_token_secret = '8R4s2og2K07pZI5VeOCQnTYyM7WZv5iBBAY7Px1bf5pKe'
# top 200 coins
limit = 500
##############################################

def scrape_twitter(coin):
    req = Request("https://coinmarketcap.com/currencies/{0}/#social".format(coin))
    response = urlopen(req, timeout=5).read().decode()
    try:
        #match twitter url
        match = p.findall(response)[0]
        #extract screen name from url
        screen_name = match.split("/")[-1]
        return screen_name
    except:
        pass

def scrape_parallel(coins, threads=4):
    #string formatting python 3.6+
    pool = ThreadPool(threads)
    results = pool.map(scrape_twitter, coins)
    pool.close()
    pool.join()
    return list(filter(lambda x: x is not None, results))

req = Request("https://api.coinmarketcap.com/v1/ticker/?limit={0}".format(limit))

#read and decode the reply
reply = urlopen(req).read().decode()

#load string as json
parsed = json.loads(reply)

#create list of coin id names [ 'bitcoin', 'ethereum', 'bitcoin-cash',....]
coinlist = [coin['id'] for coin in parsed]

#scrape the social pages threaded in parallel for faster giggles.
screen_names = scrape_parallel(coinlist)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

following = [friend.screen_name for friend in tweepy.Cursor(api.friends).items()]
for sn in screen_names:
    if sn not in following:
        try:
            api.create_friendship(screen_name=sn)
        except:
            continue
