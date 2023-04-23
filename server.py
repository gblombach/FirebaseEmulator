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
from bson.objectid import ObjectId
import json

# set mongo DB
myMongoInstance = "mongodb://34.216.225.127:27017"
#myMongoInstance = "mongodb://127.0.0.1:27017"
myMongoDB = "ZAS"
myMongoCollections = ["Alerts", "Regions", "fruit"]

# Make MongoDB Connection
mongoClient = MongoClient(myMongoInstance)
# database
db = mongoClient[myMongoDB]

app = Flask(__name__)


def format_json(data, style):
    if style == 'pretty':
        return json_util.dumps(data, sort_keys=True, indent=4)
    else:
        return json_util.dumps(data)

def parsePath(myPath):
    #strip off .json"
    temp1 = myPath.replace(".json","")
    #separate
    temp2 = temp1.split("/")
    thisCollection = temp2[0]
    if len(temp2) > 1:
        thisRecord = temp2[1]
    else:
        thisRecord = ""
    return thisCollection, thisRecord

def deleteRecord(thisCollection, thisRecord):

    collection = db[thisCollection]
    #print("delete ", thisRecord)
    if thisCollection == "Alerts":
        results = collection.delete_one({"_id": ObjectId(thisRecord)})
    else:
        results = collection.delete_one({"_id": int(thisRecord)})
    return results

def insertRecord(thisCollection, data):

    collection = db[thisCollection]
    results = collection.insert_one(data)
    return results

def updateRecord(thisCollection, thisRecord, data, upsert):

    collection = db[thisCollection]
    if upsert:
        results = collection.update_one({"_id": ObjectId(thisRecord)}, {"$set": data}, upsert)
    else:
        results = collection.update_one({"_id": ObjectId(thisRecord)}, {"$set": data})
    return results

def getQuery(thisCollection, thisRecord, orderBy, limitToFirst, limitToLast, equalTo, startAt, endAt):

    print("here: ", thisCollection, " ", thisRecord, " " , orderBy, " ", limitToFirst)
    collection = db[thisCollection]
    sort_direction = 1

    if thisRecord == "":
        match_string = {"$match": {}}
    else:
        match_string = {"$match": {"_id": thisRecord}}
    pipeline = [match_string]

    #//Todo need to test single and double quotes in curl on Ubuntu

    if orderBy is not None:
        if orderBy == "'$key'":
            sort_string = {"$sort": {"_id": sort_direction}}
            pipeline.append(sort_string)
        elif orderBy == "'$value'":
            sort_string = {"$sort": {"_id": sort_direction}}
            pipeline.append(sort_string)
        else:
            sort_string = {"$sort": {orderBy: sort_direction}}
            pipeline.append(sort_string)

        if startAt is not None:
            skip_string = {"$skip": startAt-1}
            pipeline.append(skip_string)

        if limitToFirst is not None:
            if endAt is not None:
                if endAt < limitToFirst:
                    limit_string = {"$limit": endAt}
                else:
                    limit_string = {"$limit": limitToFirst}
            else:
                limit_string = {"$limit": limitToFirst}
            print("limit_string: ", limit_string)
            pipeline.append(limit_string)

        if endAt is not None and limitToFirst is None and limitToLast is None:
            limit_string = {"$limit": endAt}
            pipeline.append(limit_string )

        if limitToLast is not None:
            limit_string = {"$limit": limitToLast}
            skip_string = {"$skip": 0}
            if endAt is not None:
                if endAt > limitToLast:
                    skip_string = {"$skip": endAt - limitToLast}
                else:
                    limit_string = {"$limit": endAt}
            else:
                temp = list(sort_string["$sort"].keys())
                pipeline.remove(sort_string)
                # print(str(temp[0]))
                # reverse order of sort, and update pipeline string
                sort_string["$sort"][str(temp[0])] = -1
                pipeline.append(sort_string)
            # print(sort_string)
            pipeline.append(skip_string)
            pipeline.append(limit_string)

        if equalTo is not None:
            match_string = {"$match": {"_id": equalTo}}
            pipeline = [match_string]



    results = collection.aggregate(pipeline)
    print("pipeline: ", str(pipeline))
    return results

def main():

    #test
    @app.route("/")
    def hello_world():
        return "<p>Hello, my world!</p>"

    @app.route('/<path:myPath>', methods=['DELETE'])
    def delete(myPath):

        thisCollection, thisRecord = parsePath(myPath)
        if thisRecord != "":
            print("ok")
            results = deleteRecord(thisCollection, thisRecord)
            return "DELETE " + str(results.acknowledged) + ": " + str(results.deleted_count)
        else:
            return "Cannot delete collection"

    @app.route('/<path:myPath>', methods=['GET'])
    def get(myPath):

        thisCollection, thisRecord = parsePath(myPath)

        orderBy = request.args.get("orderBy", type=str)
        limitToFirst = request.args.get('limitToFirst', type=int)
        limitToLast = request.args.get("limitToLast", type=int)
        equalTo = request.args.get("equalTo", type=int)
        startAt = request.args.get("startAt", type=int)
        endAt = request.args.get("endAt", type=int)
        style = request.args.get("print", type=str)
        print("limit ", limitToFirst)

        #ToDo need to move to function and address deep path
        if thisCollection not in myMongoCollections:
            results = ""
        else:
            results = getQuery(thisCollection, thisRecord, orderBy, limitToFirst, limitToLast, equalTo, startAt, endAt)
        return format_json(results, style)

    @app.route('/<path:myPath>', methods=['PATCH'])
    def patch(myPath):

        thisCollection, thisRecord = parsePath(myPath)
        content = request.get_data()
        data = json.loads(content)
        results = updateRecord(thisCollection, thisRecord, data, True)
        return "PATCH " + str(results.acknowledged) + " UpsertedID: " + str(results.upserted_id)

    @app.route('/<path:myPath>', methods=['POST'])
    def post(myPath):

        thisCollection, thisRecord = parsePath(myPath)
        content = request.get_data()
        # print(content.decode("utf-8"))
        data = json.loads(content)
        # print(format_json(data, style))
        results = insertRecord(thisCollection, data)
        # print(results)
        return "POST " + str(results.acknowledged) + " insertedID: " + str(results.inserted_id)

    @app.route('/<path:myPath>', methods=['PUT'])
    def put(myPath):

        thisCollection, thisRecord = parsePath(myPath)

        content = request.get_data()
        data = json.loads(content)
        if thisRecord == "":
            results = insertRecord(thisCollection, data)
            message = " InsertedID: " + str(results.inserted_id)
        else:
            results = updateRecord(thisCollection, thisRecord, data, False)
            message = " UpsertedID: " + str(results.upserted_id)
        return "PUT " + str(results.acknowledged) + message

if __name__ == '__main__':
    main()
    app.run(host='127.0.0.1', port=5555)
