# -*- coding: utf-8 -*-

import tweepy
import os
from airpoldata import NOX, P2, highorlow

this script runs the twitterbot
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)




airnow = ('The #airpollution now is '+ (highorlow()) + '. Particulate matter <2.5 um = ' + str(P2)+ u'µg/m³, Nitrous oxides concentration = ' + str(NOX) + u'µg/m³ #airpollution')
if os.environ.get("DEBUG"):
  print (airnow)



if P2 != None and NOX != None:
    api.update_status(status=airnow)
