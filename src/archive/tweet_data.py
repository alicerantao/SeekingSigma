import os
import tweepy as tw
import pandas as pd

consumer_key= '5MkQAtSYJtV8DWPufLhTZorwv'
consumer_secret= 'NG6WSBaLPDSZF1RTN6RGalHLX1PzS2Tomtk41zJziFLNAZjgxV'
access_token= '1296820217629347840-AHCsxL268pVnLYAaJ7TmvWZ301CnKx'
access_token_secret= 'DJQpMUxKTqh8AYCv3G5mlt1iEqmtnrGvrdIoBRx0ajS8w'

search_words = "wayfair"
date_since = "2019-01-01"
date_until = "2020-10-23"
tweet_number = 10000


def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, search_words, date_since, date_until,tweet_number):
    ## connect to twitter API
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    while(True):
        try:
            api = tw.API(auth, wait_on_rate_limit=True, timeout=1000)
            break
        except:
            continue
    # Collect tweets
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       until=date_until,
                       since=date_since).items(tweet_number)
  
    tweets_list = [[tweet.created_at, tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]
    tweets_data = pd.DataFrame(data=tweets_list, columns=['created_time', 'tweet_text', 'user', "location"])

    return tweets_data
