import socket
import http

class DSock():
    writeBuffer = ""
    readBuffer = []
    currentMessage = ""
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self):
        if len(self.sendBuffer) > 0:
            while sent != 0:
                sent = self.sock.send(self.sendBuffer.encode())
                self.sendBuffer = self.sendBuffer[sent:]
                if sent == 0:
                    print("couldn't send")
                    # raise RuntimeError("Socket connection broken")

    def receive(self):
        new = self.sock.recv(2048)
        if new == b'':
            return (b'', None, None)

        self.currentMessage += new
        head, sep, data = self.currentMessage.partition("\r\n\r\n".encode("utf-8"))

        startline, headers = http.parseRequest(head.decode("utf-8"))
        if "Content-Length" in headers:
            if len(data) >= headers['Content-length']:
                self.readBuffer.append((startline, headers, data))
                self.currentMessage = self.currentMessage[len(head) + len(sep) + len(data):]
