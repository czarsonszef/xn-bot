import tweepy
import json
from time import sleep
from googletrans import Translator

from bot_data import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

translator = Translator()

with open('last_tweet_id.json', 'r') as f:  # setup last tweeta
    f_obj = json.load(f)

skip_first_tweet = False

while True:
    if f_obj['last_tweet_id'] == '':
        public_tweets = api.home_timeline()
    else:
        public_tweets = api.home_timeline(since_id=f_obj['last_tweet_id'])
        skip_first_tweet = True

    for tweet in public_tweets[::-1]:
        if not tweet.text:  # gdy w tweecie jest tylko zdjecie
            continue

        if tweet.text[0] == 'R' and tweet.text[1] == 'T':  # zeby nie komentowalo retweetow
            continue

        if tweet.user.following == False:  # zeby nie komentowalo polecanym
            continue

        message = translator.translate(
            tweet.text, src='pl', dest='sm').text  # samoanski

        api.update_status(status='@xntentacionPL '+message,
                          in_reply_to_status_id=tweet.id)  # wyslanie tweeta

        print(log_str(tweet.text))

        f_obj['last_tweet_id'] = tweet.id_str

        with open('last_tweet_id.json', 'w') as f:
            json.dump(f_obj, f)

        sleep(10)

    print(get_time()+'Czekam...')
    sleep(180)
