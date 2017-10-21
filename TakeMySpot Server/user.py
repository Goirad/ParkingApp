import json
import time

class User:
    userID = 0
    vehicle = ""
    addr = 0
    name = ""
    lastActive = 0
    inQueue = False

    def __init__(self, userID, addr):
        with open('data.txt') as dbFile:
            db = json.load(dbFile)
            if userID in db['users']:
                self.userID = userID
                self.vehicle = db['users'][userID]['vehicle']
                self.addr = addr
                self.name = db['users'][userID]['name']
                self.lastActive = time.time()
            else:
                raise "USER NOT FOUND"



