"""
###############################
    George Blombach
    USC ID 2416-0961-99
    DSCI 551 - Spring 2023
    Firebase Emulator Project
    April, 2023

    File:   query.py
    Desc:   routine to query MongoDB running in EC2 instance
"""

from pymongo import MongoClient
from bson import json_util
import json

myMongoDB = "mongodb://34.216.225.127:27017"

# Making Connection
mongoClient = MongoClient(myMongoDB)

# database
db = mongoClient["dsci551"]

# Created or Switched to collection
Collection = db["aqi"]

# Filtering the Quantities greater
# than 40 using query.
cursor = Collection.find({"Country": "United States of America"})


def parse_json(data):
    return json_util.dumps(data)
# Printing the filtered data.

cursor = Collection.find({"Country": "United States of America"})
print(parse_json(cursor))
for record in cursor:
    print(record)

mongoClient.close()