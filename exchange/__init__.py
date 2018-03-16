from coinmarketcap import scrapeCoinCodes
import datetime

class Config:
    sizebets = 30
    base = 'btc'
    limit = 10

    apikeys = {'bittrex': {'secret': 'superbittrexsecret', 'apikey': 'secretkey'},
               'binance': {'secret': 'superbinancesecret', 'apikey': 'secretkey'},
               'huobi': {'secret': 'superhuobisecret', 'apikey': 'secretkey'},
               'okex': {'secret': 'superokexsecret', 'apikey': 'secretkey'},
               'kucoin': {'secret': 'superkucoinsecret', 'apikey': 'secretkey'}}

class Okex(Config):

    @staticmethod
    def getApiKeys():
        return Config().apikeys[__class__.__name__.lower()]

    def __init__(self):
        self.balance = self.balance(Config().base)
        self.apikeys = self.getApiKeys()

    def balance(self, coin):
        return 5

    def buy(self, coin):
        return self.apikeys

class Bittrex(Config):

    @staticmethod
    def getApiKeys():
        return Config().apikeys[__class__.__name__.lower()]

    def __init__(self):
        self.balance = self.balance(Config().base)
        self.apikeys = self.getApiKeys()

    def balance(self, coin):
        return 5

    def buy(self, coin):
        return self.apikeys

class Binance(Config):

    @staticmethod
    def getApiKeys():
        return Config().apikeys[__class__.__name__.lower()]

    def __init__(self):
        self.balance = self.balance(Config().base)
        self.apikeys = self.getApiKeys()

    def balance(self, coin):
        return 5

    def buy(self, coin):
        return self.apikeys

class Kucoin(Config):

    @staticmethod
    def getApiKeys():
        return Config().apikeys[__class__.__name__.lower()]

    def __init__(self):
        self.balance = self.balance(Config().base)
        self.apikeys = self.getApiKeys()

    def balance(self, coin):
        return 5

    def buy(self, coin):
        return self.apikeys
class Huobi(Config):

    @staticmethod
    def getApiKeys():
        return Config().apikeys[__class__.__name__.lower()]

    def __init__(self):
        self.balance = self.balance(Config().base)
        self.apikeys = self.getApiKeys()

    def balance(self, coin):
        return 5

    def buy(self, coin):
        return self.apikeys

class Router:
    def __init__(self):

        self.coinlist = scrapeCoinCodes(Config().base, Config().limit)

        self.parsers = {'BITTREX': Bittrex(),
                        'BINANCE': Binance(),
                        'KUCOIN': Kucoin(),
                        'OKEX': Okex(),
                        'HUOBI': Huobi()}

    def order(self, screen_name):
        '''accepteert twitter screen_name en koopt het op de juiste exchange'''
        for k in self.coinlist[screen_name].keys():
            try:
                if k in self.parsers and self.coinlist[screen_name][k]:
                    print(f"{datetime.datetime.now().strftime('%H:%M')} {k}, {self.parsers[k].buy(self.coinlist[screen_name][k])}, {self.coinlist[screen_name][k]}")
            except:
                continue


if __name__ == '__main__':
    b = Router()
    if 'ethereumproject' in b.coinlist:
        b.order('ethereumproject')

