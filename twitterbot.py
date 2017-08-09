import tweepy

from airpoldata import whichresult, highorlow


from keys import onsumer_key, onsumer_secret, ccess_token, ccess_token_secret

#this script runs the twitterbot

consumer_key = onsumer_key

consumer_secret = onsumer_secret

access_token = ccess_token

access_token_secret = ccess_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



def airnow():
    airnow = ("The 24hr average concententration of particulate matter below 2.5 um in Devonshire Green now is " + str(whichresult()) + 'ug/m3. This is '+ (highorlow())+' #airpollution')
    print (airnow)
    api.update_status(status=airnow)

airnow()
