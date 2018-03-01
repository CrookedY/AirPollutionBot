import tweepy
from replybot import createfinaltweet

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):

    def on_status(self, data):
        airnow = (createfinaltweet(data))
        print ('tweeting')
        print (airnow)
        api.update_status(status=airnow)

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["@shefairpol", "what's the air pollution in"])
