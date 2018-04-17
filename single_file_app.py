from urllib.request import Request, urlopen
import time
import urllib.parse
import tweepy

class TgStaticBot:
    #telegramtoken hieronder
    def __init__(self, token='509242444:TeLeGrAmToKeN'):
        self.token = token
        #chats hieronder
        self.chats = { 'lifeofcrypto': -1001141437645 }

    def send_message(self, message, name=None):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?text={urllib.parse.quote_plus(message)}&parse_mode=markdown'
        if name:
            req = Request(url+f'&chat_id={self.chats[name]}')
            reply = urlopen(req)
            print(reply.status)
            return True
        for name, chat_id in self.chats.items():
            req = Request(url+f'&chat_id={chat_id}')
            urlopen(req)


class MyStreamListener(tweepy.StreamListener):
    coinlist = [ "jemoeders_screenname", "stratis_twitter_screenname" ]
    bot = TgStaticBot()
    def on_status(self, tweet):
        tweet_dump = tweet._json
        screen_name = tweet._json['user']['screen_name']
        tweet_url = f"https://twitter.com/{screen_name}/status/{tweet.id}"
        if screen_name in self.coinlist \
                and not tweet_dump["in_reply_to_status_id"] \
                and not tweet_dump["in_reply_to_screen_name"] \
                and not tweet_dump["in_reply_to_user_id"] \
                and not tweet_dump["retweeted"]:
                        self.bot.send_message(tweet_url)
                        print(f"{line[0]} send {tweet_url} to telegram")

    def on_error(self, status_code):
        if status_code == 420:
            print("error 420")
            time.sleep(780)
            return False

if __name__ == '__main__':
    #twitterzooi hier
    consumer_key = 't4oEoD2LWV'
    consumer_secret = 'LEdr1dKAs7uZboCJ77DcCVnkTOrNXypxC5j1'
    access_token = '27631842-kSVMXD6ZJ09HdSJUZx4QSuFqdR'
    access_token_secret = '8QnTYyM7WZv5iBBAY7Px1bf5pKe'
    while True:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        try:
            myStream.userstream()
        except:
            time.sleep(60)
            continue
