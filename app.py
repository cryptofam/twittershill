import tweepy
import time
from exchange import Router

import datetime
from config import *

wordlist = ['rebrand', 'airdrop', 'news', 'partner', 'update', 'announcement', 'fork', 'listed', 'live', 'roadmap',
            'beta']

class MyStreamListener(tweepy.StreamListener):

    b = Router()
    def on_status(self, tweet):
        screen_name = tweet._json['user']['screen_name']
        if screen_name in self.b.coinlist:
            try:
                t = tweet.extended_tweet['full_text']
            except AttributeError:
                t = tweet.text
            finally:
                if any(word in t.lower() for word in wordlist):
                    print("\n")
                    for w in wordlist:
                        if w in t.lower():
                            print(f"{datetime.datetime.now().strftime('%H:%M')} found {w}")
                    print(f"{datetime.datetime.now().strftime('%H:%M')} {screen_name.upper()}")
                else:
                    print(f"{datetime.datetime.now().strftime('%H:%M')} following but no keywords{screen_name} {t}")
                self.b.order(screen_name)
                print("\n")
        else:
            print(f"{datetime.datetime.now().strftime('%H:%M')} received uninteresting tweet from {screen_name}")


    def on_error(self, status_code):
        if status_code == 420:
            print("error 420")
            time.sleep(780)
            return False


if __name__ == '__main__':

    while True:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.userstream()