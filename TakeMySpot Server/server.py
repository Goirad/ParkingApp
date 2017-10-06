#This is the server code
import time
import socket
import select 


HOST = ''
PORT = 2718
BUFSIZE = 2048

socks = [] #socket
conns = {} #{userID: (type, socket, place)}
parkers = 0
leavers = 0
#we need two things
#a list of (socket) which stores order

current_milli_time = lambda: int(round(time.time() * 1000))



def tokenize(raw_req):
  return raw_req.split(" ")



def handleRequest(sock, rawReq):
  tokens = tokenize(rawReq)
  if sock not in conns:
    #shouldn't happen
    0==0
          
  else:
    if tokens[0] == "CONNECT":
      if len(tokens) != 2:
        return "ERROR ARGS"
      else:
        userID = int(tokens[1])
        socks.append(sock)
        conns[userID] = (userID, sock, -1)
      
    elif tokens[0] == "ADDTOQUEUE":
      if len(tokens) != 2:
        return "ERROR ARGS"
      else:
        userID = int(tokens[1])

        if conns[userID][0] == "PARKER":
          return "ERROR Already in queue"
        elif conns[userID][0] == "NONE":
          conns[userID][0] = "PARKER"
          conns[userID][2] = parkers
          parkers += 1
            
    elif tokens[0] == "REMOVEFROMQUEUE":
      if len(tokens) != 2:
        return "ERROR ARGS"
      else:
        userID = int(tokens[1])
        if conns[userID][0] != "PARKER":
          return "ERROR User not parking"
        else:
          conns[userID][0] = "NONE"
          conns[userID][2] = -1
          parkers -= 1
      
    elif tokens[0] == "LEAVING":
      if len(tokens) != 1:
        return "ERROR ARGS"
      else:
        userID = int(tokens[1])

        if conns[userID][0] == "LEAVER":
          return "ERROR Already leaving"
        else:
          conns[userID][0] = "LEAVER"
          conns[userID][2] = leavers
          leavers += 1


def doLogic():
  return



serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.listen(10)



try:
    serverSock.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg))



socks.append(serverSock)

#Main Loop
while True:
    start = current_milli_time()

    readSockets, writeSockets, errorSockets = select.select(conns,[],[])
 
    for socket in readSockets:
      if socket == serverSock:
        newSock, newAddr = serverSock.accept()
        socks.append(newSock)
      else:
        reply = handleRequest(socket, socket.recv(BUFSIZE))
    
    doLogic()
    
    for socket in writeSockets:
      if socket != serverSock:
        #broadcast
        0 == 0
        
    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
time.sleep(max(1 - delta/1000, 0))





