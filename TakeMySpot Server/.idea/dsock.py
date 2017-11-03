import socket

class DSock():
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        msglen = len(msg)
        while totalsent < msglen:
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            sent += sent

    def receive(self):
        buf = self.sock.recv(2048)
        if buf == b'':
            return (b'', None, None)

        head, sep, data = buf.partition("\r\n\r\n".encode("utf-8"))
        while not sep:
            buf = buf + self.sock.recv(2048)
            head, sep, data = buf.partition("\r\n\r\n".encode("utf-8"))

        startline, headers = parseRequest(head.decode("utf-8"))
        if "Content-Length" in headers:
            while len(data) < int(headers["Content-Length"]):
                data = data + self.sock.recv(2048)

        return (startline, headers, data.decode("utf-8"))