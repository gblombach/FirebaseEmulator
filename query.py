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
from bson.objectid import ObjectId
from bson import json_util
import datetime

import json

myMongoDB = "mongodb://34.216.225.127:27017"

# Making Connection
mongoClient = MongoClient(myMongoDB)

# database
db = mongoClient["ZAS"]

# Created or Switched to collection
Collection = db["Regions"]

# Filtering the Quantities greater
# than 40 using query.
#cursor = Collection.find({"Country": "United States of America"})


def parse_json(data):
    return json_util.dumps(data)
# Printing the filtered data.

#cursor = Collection.find({})
#cursor = Collection.find({"city": "Gotham"})
cursor = Collection.find({"_id": ObjectId('64447965868c2595b29d30dd')})

#print(thisId)
#cursor = Collection.aggregate([{"$match":{"Country": "United States of America"}},{"$sort":{"Status":-1}}])
#print(parse_json(cursor))
for record in cursor:
    #thisId = record._id()
    #print(thisId)
    print(record)
results = Collection.update_one({"_id": ObjectId('64447965868c2595b29d30dd')},{"$set":{"test": "true 44"}}, False)
print(str(results.acknowledged) + " " + str(results.upserted_id))
mongoClient.close()

print(datetime.datetime.now())