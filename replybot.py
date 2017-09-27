import pandas as pd
import tweepy
import os
import string
from createlistofstations import finallist
#from airpoldata import NOX, P2, highorlow
# from nltk.tokenize import from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
from geotext import GeoText
from fuzzywuzzy import process
from geopy.geocoders import Nominatim

geolocator = Nominatim()


auth = tweepy.OAuthHandler('wA4BLtKEtSEwYZpBo3nU7swL8', 'VydrPUsMcgwbWkdVoktm5MfaZcmle8j72aO7wdF03RW50vkBbv')
auth.set_access_token('892859700819091456-IoQMfI4Bbk5E7vvNXwt8SWghl9buIq2', 'Pvd8X5lHes4mTeHsGPvaZdk1GxZ18L9WOUpoQBicKh7W0')
api = tweepy.API(auth)


searchstrings = ["@shefairpol",
                  "shefairpol",
                  "what is the air pollution in",
                  "What's the air pollution"
                  ]
tweetslookup = api.search(q="Sheffield Air Pollution")

# print (tweetslookup[1].text)

Place = GeoText(tweetslookup[0].text)
PlaceName = Place.cities[0]
location = str(PlaceName.translate(string.punctuation)) #needs to be a forloop?

#print (location)

#stationsspreadsheet = pd.read_csv("liststations.csv")
listofstations = finallist.loc[ : , "station" ]

# print (listofstations)

placeData = []

BestMatch = process.extractOne(PlaceName, listofstations)

#print(BestMatch)

###############################################################################

tweetedLocation = geolocator.geocode(location, timeout = None)

LocationCoordinates = (tweetedLocation.latitude, tweetedLocation.longitude)

print (LocationCoordinates)

ListofStationCoordinates = finallist.loc[ : , "latandlong"]

print (ListofStationCoordinates)

#for i in





# for s in tweetslookup:
#     for i in searchstrings:
#         if i == s.text:
#             sn.user.screen_name
#             reply = "@%s The air pollution now is: " % (sn)
#             s = api.update_status(reply)
#
#
# for s in tweetslookup
#     stopWords = set(stopwords.words('english'))
#     words = word_tokenise(tweetslookup)
#     wordsFiltered = []
#     for w in words:
#         if w not in stopWords:
#             wordsFiltered.append(w)
#
# for words in wordsFiltered:

    #fuzzywuzzy words in list to find words closest match to words in csv
    #tweet data from that
