import time
import socket
import sys
import Threading


current_milli_time = lambda: int(round(time.time() * 1000))

HOST = ''
PORT = 2718

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.listen(10)

try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

socket.setblocking(False)

conns = []

#Main Loop
while True:
    start = current_milli_time()

    s = True

    while s:
        try:
            conns.append(s.accept())
        except: #because we disabled blocking, this means theres none to make
            s = False


    end = current_milli_time()
    delta = (end - start)
    print("Ticked in {} ms".format(delta))
    time.sleep(max(1 - delta/1000, 0))