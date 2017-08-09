import tweepy
import os
from airpoldata import whichresult, highorlow

#this script runs the twitterbot
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

airnow = ("The 24hr average concententration of particulate matter below 2.5 um in Devonshire Green now is " + str(whichresult()) + 'ug/m3. This is '+ (highorlow())+' #airpollution')
if os.environ.get("DEBUG"):
  print (airnow)

api.update_status(status=airnow)
