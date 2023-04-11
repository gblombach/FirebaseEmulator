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

myMongoDB = "mongodb://34.216.225.127:27017"

# Making Connection
mongoClient = MongoClient(myMongoDB)

# database
db = mongoClient["dsci551"]

# Created or Switched to collection
# names: GeeksForGeeks
Collection = db["aqi"]

# Filtering the Quantities greater
# than 40 using query.
cursor = Collection.find({"Country": "United States of America"})

# Printing the filtered data.
print("The data having year greater than 40 is:")
cursor = Collection.find({"Country": "United States of America"})
#print(cursor)
for record in cursor:
    print(record)

mongoClient.close()