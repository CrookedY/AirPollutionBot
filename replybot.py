# -*- coding: utf-8 -*-
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
from geopy.distance import vincenty

geolocator = Nominatim()


auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)


searchstrings = ["@shefairpol",
                  "shefairpol",
                  "what is the air pollution in",
                  "What's the air pollution"
                  ]
tweetslookup = api.search(q="Sheffield Air Pollution")

print (tweetslookup[0].text)

Place = GeoText(tweetslookup[1].text)
PlaceNames = Place.cities
PlaceName = Place.cities[0]
location = str(PlaceName.translate(string.punctuation)) #needs to be a forloop?

print (PlaceNames)

#stationsspreadsheet = pd.read_csv("liststations.csv")
listofstations = finallist.loc[ : , "station" ]

# print (listofstations)

placeData = []

BestMatch = process.extractOne(PlaceName, listofstations)

#print(BestMatch)

###############################################################################

tweetedLocation = geolocator.geocode(location, timeout = None)

LocationCoordinates = (tweetedLocation.longitude,tweetedLocation.latitude)

print (LocationCoordinates)

ListofStationCoordinates = finallist.loc[ : , "latandlong"]

#print (ListofStationCoordinates)


shortest_distance = None
shortest_distance_coordinates = None

for station in ListofStationCoordinates:
    distance = vincenty(LocationCoordinates, station)
    if distance < shortest_distance or shortest_distance is None:
        shortest_distance = distance
        shortest_distance_coordinates = station

print (shortest_distance_coordinates)





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
