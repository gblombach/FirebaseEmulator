"""
###############################
    George Blombach
    USC ID 2416-0961-99
    DSCI 551 - Spring 2023
    Firebase Emulator Project
    April, 2023

    File:   server.py
    Description: MongoDB API using Flask
    Collections and Schema:
      CityRegion:
         _id:   <objectId>
         city:  <cityName>
         region:<regionName>
      Alerts:
         _id:   <objectId>
         timestamp: <dateTime>
         location: [{city: <cityName>, longitude, latitude
         witness:[fistname, lastname]
         image: <imageFile> (base64 encoded)
         size: rogue|pack|horde|swarm
         movement: [direction, speed]
         threat_level: low|medium|high|extreme


"""


from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util
import pymongo

# set mongo DB
myMongoInstance = "mongodb://34.216.225.127:27017"
#myMongoDB = "mongoDB://localhost:27017"
myMongoDB = "ZAS"
myMongoCollections = ["Alerts", "Regions"]

# Make MongoDB Connection
mongoClient = MongoClient(myMongoInstance)
# database
db = mongoClient[myMongoDB]

app = Flask(__name__)


def format_json(data):
    return json_util.dumps(data)


def getQuery(myPath, orderBy, limitToFirst, limitToLast, equalTo, startAt, endAt):

    print("here: ", myPath, " ", orderBy, " ", limitToFirst)
    collection = db[myPath]
    #TODO myPath
    #add paths

    match_string = {"$match": {}}
    pipeline = [match_string]



    if orderBy is not None:
        if orderBy == "$key":
            sort_string = {"$sort": {"_id": -1}}
            pipeline.append(sort_string)
        elif orderBy == "$value":
            sort_string = {"$sort": {"value": -1}}
            pipeline.append(sort_string)
        else:
            sort_string = {"$sort": {orderBy: -1}}
            pipeline.append(sort_string)

    if limitToFirst is not None:
        limit_string = {"$limit": int(limitToFirst)}
        pipeline.append(limit_string)
    if limitToLast is not None:
        limit_string = {"$limit": int(limitToLast)}
        pipeline.append(limit_string)
        #Todo set reverse sort

    if startAt is not None:
        pipeline.append()

    if endAt is not None:
        pipeline.append()

    if equalTo is not None:
        pipeline.append()

    results = collection.aggregate(pipeline)

    return results

def main():



    #test
    @app.route("/")
    def hello_world():
        return "<p>Hello, my world!</p>"

    @app.route('/<path:myPath>', methods=['DELETE'])
    def delete(myPath):
        return "Deleting"

    @app.route('/<path:myPath>', methods=['GET'])
    def get(myPath):

        orderBy = request.args.get("orderBy")
        limitToFirst = request.args.get("limitToFirst")
        limitToLast = request.args.get("limitToLast")
        equalTo = request.args.get("equalTo")
        startAt = request.args.get("startAt")
        endAt = request.args.get("endAt")
        print("limit ",limitToFirst)

        #request.args.get("orderBy")

        #results = collection.find()
        #print(format_json(results))
        if myPath not in myMongoCollections:
            results = ""
        else:
            results = getQuery(myPath, orderBy, limitToFirst, limitToLast, equalTo, startAt, endAt)
        return format_json(results)

    @app.route('/<path:myPath>', methods=['PATCH'])
    def patch(myPath):
        return "Patching"

    @app.route('/<path:myPath>', methods=['POST'])
    def post(myPath):
        return "Posting"

    @app.route('/<path:myPath>', methods=['PUT'])
    def put(myPath):
        data = {"status": "Putting"}
        return jsonify(data)


if __name__ == '__main__':
    main()
    app.run(host='127.0.0.1', port=5555)
