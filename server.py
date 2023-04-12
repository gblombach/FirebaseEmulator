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


from flask import Flask, jsonify
from pymongo import MongoClient

# set mongo DB
myMongoInstance = "mongodb://34.216.225.127:27017"
#myMongoDB = "mongoDB://localhost:27017"
myMongoDB = "ZAS"
myMongoCollection = "Alerts"



app = Flask(__name__)


def main():

    # Make MongoDB Connection
    mongoClient = MongoClient(myMongoInstance)
    # database
    db = mongoClient[myMongoDB]
    collection = db[myMongoCollection]

    #test
    @app.route("/")
    def hello_world():
        return "<p>Hello, my world!</p>"

    @app.route('/<path:myPath>', methods=['DELETE'])
    def delete(myPath):
        return "Deleting"

    @app.route('/<path:myPath>', methods=['GET'])
    def get(myPath):

        return "Getting"

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


main()
