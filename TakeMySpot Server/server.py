# This is the server code
import time
import socket
import select

HOST = ''
PORT = 27182
BUFSIZE = 2048

socks = []  # socket
conns = {}  # {userID: (type, socket, place)}
# we need two things
# a list of (socket) which stores order

current_milli_time = lambda: int(round(time.time() * 1000))


def tokenize(raw_req):
    return raw_req.decode("utf-8").strip().split(" ")


def handleRequest(sock, rawReq):
    tokens = tokenize(rawReq)
    if sock not in socks:
        # shouldn't happen
        0 == 0
        return "BLAH\n"

    else:
        if tokens[0] == "CONNECT":
            if len(tokens) != 2:
                return "ERROR ARGS\n"
            else:
                userID = int(tokens[1])
                # socks.append(sock)
                conns[userID] = ["NONE", sock, -1]
                return "SUCCESS\n"

        elif tokens[0] == "ADDTOQUEUE":
            if len(tokens) != 2:
                return "ERROR ARGS\n"
            else:
                userID = int(tokens[1])

                if conns[userID][0] == "PARKER":
                    return "ERROR Already in queue\n"
                elif conns[userID][0] == "NONE":
                    conns[userID][0] = "PARKER"
                    return "SUCCESS\n"
        elif tokens[0] == "REMOVEFROMQUEUE":
            if len(tokens) != 2:
                return "ERROR ARGS\n"
            else:
                userID = int(tokens[1])
                if conns[userID][0] != "PARKER":
                    return "ERROR User not parking\n"
                else:
                    conns[userID][0] = "NONE"
                    conns[userID][2] = -1
                    return "SUCCESS\n"
        elif tokens[0] == "LEAVING":
            if len(tokens) != 1:
                return "ERROR ARGS\n"
            else:
                userID = int(tokens[1])

                if conns[userID][0] == "LEAVER":
                    return "ERROR Already leaving\n"
                else:
                    conns[userID][0] = "LEAVER"
                    return "SUCCESS\n"
        else:
            return "INVALID COMMAND\n"


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

    readSockets, writeSockets, errorSockets = select.select(socks, [], [], .5)

    for socket in readSockets:
        if socket == serverSock:
            newSock, newAddr = serverSock.accept()
            socks.append(newSock)
            print("new connection")
        else:
            reply = handleRequest(socket, socket.recv(BUFSIZE))
            socket.send(str.encode(reply))

    doLogic()

    for socket in writeSockets:
        if socket != serverSock:
            # broadcast
            0 == 0

    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
    time.sleep(max(1 - delta / 1000, 0))




