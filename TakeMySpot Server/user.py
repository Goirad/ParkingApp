import json
import time
from enum import Enum


current_milli_time = lambda: int(round(time.time() * 1000))

successReply = (200, json.dumps({'success' : True}))


class State(Enum):
    START = 6
    PARKING = 0
    LEAVING= 1
    MATCHED_P = 2
    MATCHED_L = 3
    EXCHANGING_P = 4
    EXCHANGING_L = 5



class User:
    state = State.START
    sock = None
    lastActive = 0
    server = None

    match = None
    declinedMatches = []

    userID = 0
    vehicle = ""
    name = ""

    reply = None

    def __init__(self, userID, sock, server):
        with open('data.txt') as dbFile:
            db = json.load(dbFile)
            if userID in db['users']:
                self.userID = userID
                self.server = server
                self.vehicle = db['users'][userID]['vehicle']
                self.sock = sock
                self.state = State.START
                self.name = db['users'][userID]['name']
                self.lastActive = current_milli_time()
            else:
                raise "USER NOT FOUND"

    def handleParking(self, argsDict):

        self.lastActive = current_milli_time()

        if self.state != State.START:
            self.reply = self.server.makeError('That command is not available for this user state')
        else:
            self.state = State.PARKING
            server.startQueue.append(self)
            self.reply = successReply

    def handleLeaving(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state != State.START:
            self.reply = self.server.makeError('That command is not available for this user state')
        else:
            self.state = State.LEAVING
            self.server.leaveQueue.append(self)
            self.reply = successReply



    def match(self, matchUser):
        if self.state == State.LEAVING:
            self.state = State.MATCHED_L
            self.match = matchUser
        elif self.state == State.PARKING:
            self.state = State.MATCHED_P
            self.match = matchUser


    def handleAccept(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state == State.MATCHED_P:
            self.state = State.EXCHANGING_P
            self.reply = successReply

        elif self.state == State.MATCHED_L:
            self.state = State.EXCHANGING_L
            self.reply = successReply
        else:
            self.reply = self.server.makeError('That command is not available for this user state')




    def handleDecline(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state == State.MATCHED_L:
            self.state = State.LEAVING
            self.declinedMatches.append(self.match)
            self.match = None
            self.reply = successReply

        #TODO Evaluate whether it is appropriate to have a parked person decline a parker
        elif self.state == State.MATCHED_P:
            self.state = State.PARKING
            self.declinedMatches.append(self.match)
            self.match = None
            self.reply = successReply

        else:
            self.reply = self.server.makeError('That command is not available for this user state')



    def handleSuccess(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state == State.EXCHANGING_P or State.EXCHANGING_L:
            self.state = State.START
            self.match = None

            if self.state == State.EXCHANGING_P:
                self.server.parkingQueue.remove(self)
            elif self.state == State.EXCHANGING_L:
                self.server.leavingQueue.remove(self)
            self.reply = successReply
        else:
            self.reply = self.server.makeError('That command is not available for this user state')


    def handleFailure(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state == State.EXCHANGING_P:
            self.state = State.PARKING
            self.match = None
            self.reply = successReply

        elif self.state == State.EXCHANGING_L:
            self.state = State.LEAVING
            self.match = None
            self.reply = successReply
        else:
            self.reply = self.server.makeError('That command is not available for this user state')



    def handleCancel(self, argsDict):
        self.lastActive = current_milli_time()

        if self.state == State.LEAVING:
            self.state = State.START
            self.server.leavingQueue.remove(self)
            self.reply = successReply

        elif self.state == State.PARKING:
            self.state = State.START
            self.server.parkingQueue.remove(self)
            self.reply = successReply

        elif self.state == State.EXCHANGING_P:
            self.state = State.START
            self.match = None
            self.server.parkingQueue.remove(self)
            self.reply = successReply

        elif self.state == State.EXCHANGING_L:
            self.state = State.START
            self.match = None
            self.server.leavingQueue.remove(self)
            self.reply = successReply
        else:
            self.reply = self.server.makeError('That command is not available for this user state')

    def updateReply(self, positionInQueue):
        self.reply = (200, json.dumps({'position': positionInQueue}))