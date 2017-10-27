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



# we need two things
# a list of (socket) which stores order

expectedJSONArgs = {
    'create' : ['userID', 'name', 'vehicle'],
    'default': ['userID']
}

current_milli_time = lambda: int(round(time.time() * 1000))


def parse(raw_req):
    return json.loads(raw_req)


def makeError(err):
    print("error", err)
    return (404, json.dumps({'success': False, 'description': err}))


def checkArgs(reqJSON, fun):
    if reqJSON.keys != expectedJSONArgs[fun]:
        return True
    else:
        return makeError('Invalid arguments for ' + fun)

class Server:
    leavingQueue = []
    parkingQueue = []

    socks = []  # socket
    conns = {}  # {userID: user}
    sockAddr = {}  # {socket: user}
    def handleConnect(self, addr, req):
        res = checkArgs(req, 'default')
        if res == True:
            userID = req['userID']
            if userID in self.conns:
                return makeError('User already connected')
            else:
                try:
                    user = User(userID, addr, self)
                    self.conns[userID] = user
                    self.sockAddr[addr] = user
                    user.reply = (200, json.dumps({'success' : True}))
                except Exception as e:
                    print(e)
                    return makeError('User not found')
        else:
            return res



    def handleDisconnect(self, addr, req):
        res = checkArgs(req, 'default')
        if res == True:
            userID = req['userID']
            #TODO implement dequeuing and elegant cleanup
            if userID in self.conns:
                del self.sockAddr[self.conns[userID].addr]
                del self.conns[userID]

                return (200, json.dumps({'success': True}))
            else:
                return makeError('User not connected')
        else:
            return res


    def handleCreate(self, req):
        res = checkArgs(req, 'create')
        if res == True:
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
        else:
            return res

    def handleRequest(self, sock, rawReq, page):
        try:
            req = parse(rawReq)
        except Exception as e:
            print(e)
            return makeError('Invalid JSON')

        if 'userID' not in req:
            return makeError('Who is talking to me?')
        else:

            if page == '/connect':
                res = checkArgs(req, 'default')
                if res == True:
                    self.handleConnect(sock, req)
                else:
                    return res
            elif page == '/create':
                res = checkArgs(req, 'create')
                if res == True:
                    self.handleCreate(req)
                else:
                    return res
            else:
                if req['userID'] not in self.conns:
                    return makeError('That user is not connected')
                else:
                    if page == '/park':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.conns[req['userID']].handleParking(req)
                        else:
                            return res
                    elif page == '/leave':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.conns[req['userID']].handleLeaving(req)
                        else:
                            return
                    elif page == '/disconnect':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.handleDisconnect(sock, req)
                        else:
                            return res
                    elif page == '/cancel':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.conns[req['userID']].handleCancel(req)
                        else:
                            return res
                    elif page == '/accept':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.conns[req['userID']].handleCancel(req)
                        else:
                            return res
                    elif page == '/decline':
                        res = checkArgs(req, 'default')
                        if res == True:
                            self.conns[req['userID']].handleCancel(req)
                        else:
                            return res
                    else:
                        return makeError('Invalid command')


    # Once all of last second's requests have been processed, do all the logic
    def doLogic(self):
        #check for timeouts
        '''
        for user in conns:
            #TODO make this a more graceful disconnect
            if current_milli_time() - conns[user].lastActive > 30_000:
                del conns[user]
        '''

        #update queue positions
        for idx, user in enumerate(self.parkingQueue):
            user.updateReply(idx)
        #TODO check for matches
        return

    def __init__(self):
        import socket
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            serverSock.bind((HOST, PORT))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg))

        serverSock.listen(10)
        self.socks.append(serverSock)

        # Main Loop

        while True:
            start = current_milli_time()

            readSockets, writeSockets, errorSockets = select.select(self.socks, self.socks, [], .02)

            for socket in readSockets:
                if socket == serverSock:
                    newSock, newAddr = serverSock.accept()
                    self.socks.append(newSock)
                    self.sockAddr[newSock] = newAddr
                    print("new connection")
                else:
                    startline, headers, data = http.recvFullMessage(socket)
                    print(data)
                    if startline == b'':
                        self.socks.remove(socket)
                        if socket in self.conns:
                            #TODO more graceful sudden disconnect
                            del self.conns[socket]
                    else:
                        print('Request: \n' + startline)
                        page, querydict = http.parseStartLine(startline)

                        self.handleRequest(socket, data, page)

            for socket in writeSockets:
                if socket != serverSock and socket in self.sockAddr:
                    user = self.sockAddr[socket]
                    if user.reply != None:
                        code, reply = user.reply

                        httpReply = http.getResponseHead({}, code=str(code), data=reply)
                        http.sendFullMessage(socket, httpReply.encode("utf-8"))
                        user.reply = None

            self.doLogic()

            end = current_milli_time()
            delta = (end - start)
            print("Ticked in {} ms".format(delta))
            time.sleep(max(1 - delta / 1000, 0))

s = Server()