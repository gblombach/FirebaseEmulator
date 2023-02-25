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

# Making Connection
myclient = MongoClient("mongodb://34.216.225.127:27017")

# database
db = myclient["video"]

# Created or Switched to collection
# names: GeeksForGeeks
Collection = db["movies"]

# Filtering the Quantities greater
# than 40 using query.
#cursor = Collection.find({"year": {"$gt": 40}})

# Printing the filtered data.
print("The data having year greater than 40 is:")
cursor = Collection.find()
#print(cursor)
for record in cursor:
    print(record)

myclient.close()