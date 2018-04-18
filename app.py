############### https://python-forum.io/Thread-Basic-Part-1-Python-3-6-and-pip-installation-under-Windows
import tweepy##
###############
from urllib.request import Request, urlopen
import time

#https://t.me/botfather
telegramToken = "telegram-token_here"
telegramChats = {
    #https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
    "lifeofcrypto": -1001141437645,
    "another_roomname": -1231321,
    "some_user": 12321312
}

#https://developer.twitter.com
twitterConsumerKey = "t4oEoD14kAlmbAG"
twitterConsumerSecret = "LEdr1dOrNXypxC5j1"
twitterAccessToken = "276318x4QSuFqdR"
twitterAccessTokenSecret = "8R4s7Px1bf5pKe"

triggerScreenNames = ["twitter_handle", "another_twitter_handle"]
triggerWordlist = ["rebrand", "airdrop", "fork", "swap", "presale", "major", "partner"]

def sendTgMessage(message):
    url = f"https://api.telegram.org/bot{telegramToken}/sendMessage?text={urllib.parse.quote_plus(message)}&parse_mode=markdown"
    for name, chatId in telegramChats.items():
        try:
            req = Request(url+f"&chat_id={chatId}")
            urlopen(req)
        except Exception as e:
            print(f"kan geen telegram bericht sturen naar {name}")
            print(e)

def checkTweetCriteria(tweet):
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    '''accepteert een tweepy Tweet Object en
    controleert of deze voldoet aan gestelde criteria'''

    if not tweet._json["user"]["screen_name"] in triggerScreenNames: return False
    if tweet._json["retweeted"]: return False
    if tweet._json["in_reply_to_status_id"]: return False
    if tweet._json["in_reply_to_user_id"]: return False

    try:
        if not any(word.lower() in tweet.extended_tweet["full_text"].lower() for word in triggerWordList): return False
    except AttributeError:
        if not any(word.lower() in tweet.text.lower() for word in triggerWordList): return False
    finally:
        return True


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        if checkTweetCriteria(tweet):
            sendTgMessage(f"https://twitter.com/{tweet._json['user']['screen_name']}/status/{tweet.id}")

    def on_error(self, status_code):
        raise AttributeError(f"error status code {status_code}")



        
if __name__ == '__main__':
    while True:
        auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
        auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        try:
            myStream.userstream()
        except AttributeError as e:
            print(e)
            time.sleep(780)
            continue
        except Exception as e:
            print("critical error")
            print(e)
            exit(1)
