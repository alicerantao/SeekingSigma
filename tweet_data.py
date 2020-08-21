import os
import tweepy as tw
import pandas as pd

def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, search_words, date_since, tweet_number):
    ## connect to twitter API
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    # Collect tweets
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       since=date_since).items(tweet_number)
  
    tweets_list = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]
    
    tweets_data = pd.DataFrame(data=tweets_list, columns=['tweet_text', 'user', "location"])

    return tweets_data
