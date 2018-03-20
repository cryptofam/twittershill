import tweepy
import time
from exchange import Router

import datetime
from config import *

wordlist = ['rebrand', 'airdrop', 'partner',  'announcement', 'fork', 'beta']
print(f"filtering on word {' '.join(wordlist)}")


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
                    print(f"{datetime.datetime.now().strftime('%H:%M')} {screen_name.upper()}: \n{datetime.datetime.now().strftime('%H:%M')} {t} ")
                self.b.order(screen_name)
                print("\n")

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