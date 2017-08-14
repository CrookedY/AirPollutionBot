import tweepy
import os
from airpoldata import NOX, P2, highorlow

#this script runs the twitterbot
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

airnow = ('The air pollution now is '+ (highorlow()) + '. Particulate matter <2.5 um = ' + str(P2)+ 'ug/m3, Nitrous oxides concentration = ' + str(NOX) + 'ug/m3 #airpollution')
if os.environ.get("DEBUG"):
  print (airnow)

print airnow

api.update_status(status=airnow)
