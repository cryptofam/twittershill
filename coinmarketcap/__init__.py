from urllib.request import Request, urlopen
from multiprocessing.pool import ThreadPool
import json
import re

def scrape_twitter(coin):
    '''scrapes the twitter screen name and Bittrex coincode'''
    req = Request("https://coinmarketcap.com/currencies/{0}/#markets".format(coin))
    response = urlopen(req, timeout=15).read().decode()
    result = {}
    for x in regexen_compiled:
        try:
            result[x] = regexen_compiled[x].findall(response)[0]
        except:
            result[x] = None
    return result

unsupported = []
def scrape_parallel(coins, threads=8):
    result = {}
    pool = ThreadPool(threads)
    results = pool.map(scrape_twitter, coins)
    #results list is formatted like this now {'BITTREX': None, 'BINANCE': None, 'TWITTER': 'telcoin_team'},
    pool.close()
    pool.join()
    for frame in results:
        if frame['TWITTER'] == None:
            continue
        screen_name = frame['TWITTER']
        frame.pop('TWITTER', None)
        if not all(value == None for value in frame.values()):
            result[screen_name] = frame
        else:
            unsupported.append(screen_name)
    #result list is formatted like this now {'ethereumproject': {'BITTREX': 'BTC-ETH', 'BINANCE': 'ETH_BTC'},
    return result

regexen_compiled = {}
def scrapeCoinCodes(base, limit):
    regexen = {
        'BITTREX': f'''<a href=\"https:\/\/bittrex.com\/Market\/Index\?MarketName=(.*{base}.*)" ''',
        'BINANCE': f'''<a href=\"https:\/\/www.binance.com\/trade.html\?symbol\=(.*{base}.*)" ''',
        'KUCOIN': f'''<a href=\"https:\/\/www.kucoin.com\/\#\/trade\/(.*{base}.*)" ''',
        'HUOBI': f'''<a href=\"https:\/\/www.huobi.pro\/ko\-kr\/(.*{base}.*)\/exchange" ''',
        'OKEX': f'''<a href=\"https:\/\/www.okex.com\/spot\/trade\/index.do\#(.*{base}.*)" ''',
        'TWITTER': '''<a\sclass=\"twitter-timeline\" href=\"https:\/\/twitter.com\/(.*)\" data-widget'''
    }

    for x in regexen:
        regexen_compiled[x] = re.compile(regexen[x], re.IGNORECASE)
    req = Request("https://api.coinmarketcap.com/v1/ticker/?limit={0}".format(limit))
    reply = urlopen(req).read().decode()
    parsed = json.loads(reply)

    #create list of coin id names [ 'bitcoin', 'ethereum', 'bitcoin-cash',....]
    coinlist = [coin['id'] for coin in parsed]

    #scrape the social pages threaded in parallel for faster giggles.
    paired_list = scrape_parallel(coinlist)
    return paired_list

if __name__ == '__main__':
    ##############################################
    # top 200 coins
    limit = 100
    ##############################################
    # base currency
    base = 'eth'
    t = scrapeCoinCodes(base, limit)
    print(t)