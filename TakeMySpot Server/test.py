from dsock import DSock
import json

sock = DSock()

sock.connect('127.0.0.1', 27182)
mes = json.dumps({'userID' : 'Dario', 'password': 'dario'})
sock.sendBuffer += ""
sock.send()
print(sock.currentMessage)