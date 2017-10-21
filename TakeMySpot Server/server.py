# This is the server code

import socket
import time
import select
from user import User
import json
import os
import http

HOST = ''
PORT = 27182
BUFSIZE = 2048

queue = []
socks = []  # socket
conns = {}  # {userID: user}
sockAddr = {}  # {socket: (host, port)}
# we need two things
# a list of (socket) which stores order

current_milli_time = lambda: int(round(time.time() * 1000))


def parse(raw_req):
    return json.loads(raw_req)


def makeError(err):
    print("error", err)
    return (404, json.dumps({'success': False, 'description': err}))


def handleConnect(addr, req):
    if len(req) != 1 or 'userID' not in req:
        return makeError('Invalid command arguments')
    else:
        userID = req['userID']
        if userID in conns:
            return makeError('User already connected')
        else:
            try:
                user = User(userID, addr)
                conns[userID] = user
                return (200, json.dumps({'success': True, 'name': user.name, 'vehicle': user.vehicle}))
            except Exception as e:
                print(e)
                return makeError('User not found')


def handleDisconnect(addr, req):
    if len(req) != 1 or 'userID' not in req:
        return makeError('Invalid command arguments')
    else:
        userID = req['userID']
        if userID in conns:
            del conns[userID]
            return (200, json.dumps({'success': True}))
        else:
            return makeError('User not connected')


def handleCreate(req):
    if len(req) != 3 or 'userID' not in req or 'name' not in req or 'vehicle' not in req:
        return makeError('Invalid command arguments')
    else:
        dbFile = open('data.txt', 'r')
        db = json.load(dbFile)
        if req['userID'] in db['users']:
            return makeError('User already exists')
        else:
            userID = req['userID']
            vehicle = req['vehicle']
            name = req['name']

            db['users'][userID] = {'vehicle': vehicle, 'name': name}

            new = open('data1.txt', 'w')

            json.dump(db, new, indent=4)

            dbFile.close()
            new.close()

            os.rename('data.txt', 'data2.txt')
            os.rename('data1.txt', 'data.txt')
            os.rename('data2.txt', 'data1.txt')

            return (200, json.dumps({'success': True}))


def handlePark(req):
    if len(req) != 1 or 'userID' not in req:
        return makeError('Invalid command arguments')
    else:
        userID = req['userID']
        if userID not in conns:
            return makeError('User not connected')
        else:
            user = conns[userID]
            user.lastActive = current_milli_time()
            user.parking = True
            queue.append(user)

            return (200, json.dumps({'success': True}))


def handleLeave(req):
    if len(req) != 2 or 'userID' not in req or 'locationDescription' not in req:
        return makeError('Invalid command arguments')
    else:
        userID = req['userID']
        if userID not in conns:
            return makeError('User not connected')
        else:
            user = conns[userID]
            user.lastActive = current_milli_time()
            if len(queue) == 0:
                return makeError('No one wants to park')
            else:
                nextInLine = queue[0]
                nextInLine.matched = True
                nextInLine.matchUserID = userID
                nextInLine.matchLocation = req['locationDescription']
                return (200, json.dumps({'success': True, 'matchUserID': nextInLine.userID}))


def handleAccept(req):
    return


def handleDecline(req):
    return


def handlePoll(req):
    if len(req) != 1 or 'userID' not in req:
        return makeError('Invalid command arguments')
    else:
        userID = req['userID']
        if userID not in conns:
            return makeError('User not connected')
        else:
            user = conns[userID]
            user.lastActive = current_milli_time()
            reply = {'userID': userID, 'inQueue': user.inQueue}
            if user.inQueue:
                reply['matched'] = user.matched
                reply['position'] = user.matchLocation
                if user.matched:
                    reply['matchUserID'] = user.matchUserID
                    reply['matchLocation'] = user.matchLocation


# TODO check user is connected here not in each request method
def handleRequest(addr, rawReq, page):
    try:
        req = parse(rawReq)
    except Exception as e:
        print(e)
        return makeError('Invalid JSON')

    if page == '/connect':
        return handleConnect(addr, req)
    elif page == '/create':
        return handleCreate(req)
    else:
        return makeError('Invalid command')


# Once all of last second's requests have been processed, do all the logic
def doLogic():
    for user in conns:
        if time.time() - conns[user].lastActive > 30:
            del conns[user]
    return


serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    serverSock.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg))

serverSock.listen(10)
socks.append(serverSock)

# Main Loop

while True:
    start = current_milli_time()

    readSockets, writeSockets, errorSockets = select.select(socks, [], [], .01)

    for socket in readSockets:
        if socket == serverSock:
            newSock, newAddr = serverSock.accept()
            socks.append(newSock)
            sockAddr[newSock] = newAddr
            print("new connection")
        else:
            startline, headers, data = http.recvFullMessage(socket)
            print(data)
            if startline == b'':
                socks.remove(socket)
                if socket in conns:
                    del conns[socket]
            else:
                print('Request: \n' + startline)
                page, querydict = http.parseStartLine(startline)

                code, reply = handleRequest(sockAddr[socket], data, page)

                httpReply = http.getResponseHead({}, code=str(code), data=reply)
                http.sendFullMessage(socket, httpReply.encode("utf-8"))

    doLogic()

    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
time.sleep(max(1 - delta / 1000, 0))