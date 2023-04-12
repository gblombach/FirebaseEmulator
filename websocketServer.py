"""
###############################
    George Blombach
    USC ID 2416-0961-99
    DSCI 551 - Spring 2023
    Firebase Emulator Project
    April, 2023

    File:   websocketServer.py
"""

import asyncio
import datetime
import random
import websockets


async def time(websocket, path):
    print("new connection path " + path)
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print(now)
        await websocket.send(now)
        await asyncio.sleep(10)

start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()