"""
###############################
    George Blombach
    USC ID 2416-0961-99
    DSCI 551 - Spring 2023
    Firebase Emulator Project
    April, 2023

    File:   websocketServer.py
    Description:
            Websocket server listening on IP 127.0.0.1, port 5678
"""

import asyncio
import datetime
import websockets
from pymongo import MongoClient

# set mongo DB
myMongoInstance = "mongodb://34.216.225.127:27017"
#myMongoDB = "mongoDB://localhost:27017"
myMongoDB = "ZAS"
myMongoCollection = "Alerts"


async def get_insert():

    # Make MongoDB Connection
    mongoClient = MongoClient(myMongoInstance)
    # database
    db = mongoClient[myMongoDB]
    collection = db[myMongoCollection]

    change_stream = collection.watch([{"$match": {"operationType": "insert"}}])
    for change in change_stream:
        message = change["fullDocument"]
        timestamp = message["timestamp"]
        location = message["location"]
        latitude = location["latitude"]
        longitude = location["longitude"]
        locale = location["locale"]
        scale = message["scale"]
        direction = message["direction"]
        speed = message["speed"]
        threat_level = message["treat_level"]
        #for item in message:
        #    print(str(item))
        print(latitude, " ", longitude)
        return str(latitude), " ", str(longitude)


async def send_alert(websocket, path):
    print("new connection path " + path)

    while True:
        #await websocket.send(now)
        await websocket.send(await get_insert())
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print(now)
        await asyncio.sleep(0)

start_server = websockets.serve(send_alert, '127.0.0.1', 5678)
#start_server = websockets.serve(send_alert, '34.216.225.127', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()