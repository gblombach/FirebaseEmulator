"""
###############################
    George Blombach
    USC ID 2416-0961-99
    DSCI 551 - Spring 2023
    Firebase Emulator Project
    April, 2023

    File:   server.py
    Description: MongoDB API using Flask
"""


from flask import Flask

app = Flask(__name__)


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
    return "Putting"
