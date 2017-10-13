import json

class User:
    userID = 0
    vehicle = ""
    sock = 0
    name = ""

    def __init__(self, userID, sock):
        with open('data.txt') as dbFile:
            db = json.load(dbFile)
            if userID in db['users']:
                self.userID = userID
                self.vehicle = db['users'][userID]['vehicle']
                self.sock = sock
                self.name = db['users'][userID]['name']
            else:
                raise "USER NOT FOUND"



