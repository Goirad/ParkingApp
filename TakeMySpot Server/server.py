# This is the server code

import socket
import time
import select
from user import User
import json
import os

HOST = ''
PORT = 27182
BUFSIZE = 2048

socks = []  # socket
conns = {}  # {socket: user}
# we need two things
# a list of (socket) which stores order

current_milli_time = lambda: int(round(time.time() * 1000))


def parse(raw_req):
    return json.loads(raw_req.decode("utf-8"))


def makeError(err):
    return json.dumps({'reply' : 'error', 'description' : err})

def handleConnect(sock, req):
    if len(req) != 2 or 'userID' not in req:
        return makeError('Invalid command arguments')
    else:
        try:
            user = User(req['userID'], sock)
            conns[sock] = user
            return json.dumps({'reply': 'success', 'name' : user.name, 'vehicle' : user.vehicle})
        except Exception as e:
            print(e)
            return makeError('User not found')

def handleCreate(sock, req):
    if len(req) != 4 or 'userID' not in req or 'name' not in req or 'vehicle' not in req:
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

            db['users'][userID] = {'vehicle' : vehicle, 'name': name}

            new = open('data1.txt', 'w')

            json.dump(db, new, indent=4)

            dbFile.close()
            new.close()

            os.rename('data.txt', 'data2.txt')
            os.rename('data1.txt', 'data.txt')
            os.rename('data2.txt', 'data1.txt')

            return json.dumps({'reply' : 'success'})

def handleRequest(sock, rawReq):
    try:
        req = parse(rawReq)
    except:
        return makeError('Invalid JSON')

    if 'command' not in req:
        return makeError('Command field not found')
    else:

        if req['command'] == "connect":
            return handleConnect(sock, req)
        elif req["command"] == "create":
            return handleCreate(sock, req)
        else:
            return makeError('Invalid command')


# Once all of last second's requests have been processed, do all the logic
def doLogic():
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
            print("new connection")
        else:
            request = socket.recv(BUFSIZE)
            if request == b'':
                socks.remove(socket)
                if socket in conns:
                    del conns[socket]
            else:
                print('Request: \n' + request.decode('utf-8'))
                reply = handleRequest(socket, request)
                socket.send(str.encode(reply + "\n"))

    doLogic()


    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
    time.sleep(max(1 - delta / 1000, 0))




