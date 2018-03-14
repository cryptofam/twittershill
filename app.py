from urllib.request import Request, urlopen
from multiprocessing.pool import ThreadPool
import json
import re
import tweepy
import time


#nasty regex for grabbing the urls
base = 'btc'
#this script collect matches the
regexen = {
    'BITTREX': f'''<a href=\"https:\/\/bittrex.com\/Market\/Index\?MarketName=(.*{base}.*)" ''',
    'BINANCE': f'''<a href=\"https:\/\/www.binance.com\/trade.html\?symbol\=(.*{base}.*)" ''',
    'HUOBI': f'''<a href=\"https:\/\/www.huobi.pro\/ko\-kr\/(.*{base}.*)\/exchange" ''',
    'OKEX': f'''<a href=\"https:\/\/www.okex.com\/spot\/trade\/index.do\#(.*{base}.*)" ''',
    'KUCOIN': f'''<a href=\"https:\/\/www.kucoin.com\/\#\/trade\/(.*{base}.*)" ''',
    'TWITTER': '''<a\sclass=\"twitter-timeline\" href=\"https:\/\/twitter.com\/(.*)\" data-widget'''
}
regexen_compiled = {}
for x in regexen:
    regexen_compiled[x] = re.compile(regexen[x], re.IGNORECASE)

##############################################
# top 200 coins
limit = 200
##############################################

def scrape_twitter(coin):
    '''scrapes the twitter screen name and Bittrex coincode'''
    req = Request("https://coinmarketcap.com/currencies/{0}/#markets".format(coin))
    response = urlopen(req, timeout=10).read().decode()
    result = {}
    for x in regexen_compiled:
        try:
            result[x] = regexen_compiled[x].findall(response)[0]
        except:
            result[x] = None
    return result


def scrape_parallel(coins, threads=4):
    result = {}
    #string formatting python 3.6+
    pool = ThreadPool(threads)
    results = pool.map(scrape_twitter, coins)
    #results list is formatted like this now {'BITTREX': None, 'BINANCE': None, 'TWITTER': 'telcoin_team'},
    pool.close()
    pool.join()
    for frame in results:
        screen_name = frame['TWITTER']
        frame.pop('TWITTER', None)
        if screen_name:
            if not all(value == None for value in frame.values()):
                result[screen_name] = frame
            else:
                print(f"don't support {screen_name} yet")
    #result list is formatted like this now {'ethereumproject': {'BITTREX': 'BTC-ETH', 'BINANCE': 'ETH_BTC'},
    return result

class MyStreamListener(tweepy.StreamListener):
    global fixed_list

    def on_status(self, tweet):
        wordlist = ['rebrand', 'airdrop', 'partner', 'update', 'announcement', 'fork']
        if not tweet._json['retweeted']:
            screen_name = tweet._json['user']['screen_name']
            if screen_name in fixed_list:
                try:
                    t = tweet.extended_tweet['full_text']
                except AttributeError:
                    t = tweet.text
                finally:
                    if any(word in t.lower() for word in wordlist):
                        print("found something cool shoopdawoop")
                        print(t)
                        print(fixed_list[screen_name])
                        print("found something cool shoopdawoop")

    def on_error(self, status_code):
        if status_code == 420:
            print("error 420")
            time.sleep(780)
            return False


if __name__ == '__main__':
    req = Request("https://api.coinmarketcap.com/v1/ticker/?limit={0}".format(limit))

    #read and decode the reply
    reply = urlopen(req).read().decode()

    #load string as json
    parsed = json.loads(reply)

    #create list of coin id names [ 'bitcoin', 'ethereum', 'bitcoin-cash',....]
    coinlist = [coin['id'] for coin in parsed]

    #scrape the social pages threaded in parallel for faster giggles.
    fixed_list = scrape_parallel(coinlist)
    print(f"searching for top {limit} coins")
    print(f"found {len(fixed_list)} coins")

    while True:

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.userstream()