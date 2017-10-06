#This is the server code
import time
import socket
import select 


HOST = ''
PORT = 2718
BUFSIZE = 2048

Queue = [] #socket
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
    if tokens[0] == "CONNECT":
      if len(tokens) != 2:
        return "ERROR ARGS"
      else:
        userID = int(tokens[1])
        conns[userID] = (userID, sock, -1)
          
  else:
    if tokens[0] == "CONNECT":
      return "ERROR DUP USER"
      
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






serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.listen(10)



try:
    serverSock.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg))



conns.append(serverSock)

#Main Loop
while True:
    start = current_milli_time()

    readSockets, writeSockets, errorSockets = select.select(conns,[],[])
 
    for socket in read_sockets:
      if socket == serverSock:
        newSock, newAddr = serverSock.accept()
        conns.append(newSock)
      else:
        reply = handleRequest(socket, socket.recv(BUFSIZE))
    
    for socket in writeSockets:
      if socket != serverSock:
        
        
        
    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
time.sleep(max(1 - delta/1000, 0))





