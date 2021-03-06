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

while True:
    try:
        if f_obj['last_tweet_id'] == '':
            public_tweets = api.home_timeline()
        else:
            public_tweets = api.home_timeline(since_id=f_obj['last_tweet_id'])

        for tweet in public_tweets[::-1]:
            # czasem sie pojawiaja w home_timeline() jakies stare tweety
            if get_time()['day_int']-tweet.created_at.day > 2 or (get_time()['day_int']-tweet.created_at.day <= -28 and get_time()['day_int']-tweet.created_at.day >= -30):
                continue
            if not tweet.text:  # gdy w tweecie jest tylko zdjecie
                continue
            if tweet.text[:2] == 'RT':  # zeby nie komentowalo retweetow
                continue
            if not tweet.user.following:  # zeby nie komentowalo polecanym
                continue

            message = translator.translate(
                tweet.text, src='pl', dest='sm').text  # samoanski
            api.update_status(status=f'@xntentacionPL {message}',
                              in_reply_to_status_id=tweet.id)  # wyslanie tweeta
            api.create_favorite(tweet.id)

            log(tweet.text)

            f_obj['last_tweet_id'] = tweet.id_str
            append_json('last_tweet_id.json', f_obj)
            sleep(10)
    except BaseException as e:
        handle_error(e)

    print(f'{get_time()["log_string"]}Czekam...')
    sleep(180)
