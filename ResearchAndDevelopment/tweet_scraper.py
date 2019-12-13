import tweepy
import codecs
import csv


#### Code that gathers 3000 tweets on a specific hashtag, using Twitter API. Writes to csv file.

consumer_key = #yourkey
consumer_secret = #yoursecret
access_token = #yourtoken
access_token_secret = #yoursecret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

csvFile = codecs.open('scraped_tweets.csv', 'a', encoding='ascii', errors='ignore')
csvwriter = csv.writer(csvFile)


tweets= tweepy.Cursor(api.search, q="#MeToo -filter:retweets",tweet_mode="extended", count=100, 
                           lang="en",since = "2018-10-05",
                           until = "2018-10-06").items(3000) #change these if you need more, or you need other dates.
for item in tweets:
    csvwriter.writerow([item.user.screen_name.encode("utf-8"),\
                        item.full_text.encode("utf-8"),\
                        item.user.followers_count]) #writes the tweets plus some extra information


