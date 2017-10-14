# TCPServer.py

from socket import socket, SOCK_STREAM, AF_INET, SHUT_WR
from time import strftime, gmtime, strptime
import os
import sys




mimetypes = {"": "", "txt": "text/plain", "html": "text/html", "jpg": "image/jpeg", "ico": "image/x-icon",
             "/": "text/html", "py": "text"}


def parseRequest(request):
    headersraw = request.split("\r\n")
    startline = headersraw[0]
    headersraw = headersraw[1:]
    headers = {}
    for header in headersraw:
        title, sep, value = header.partition(":")
        headers[title] = value.strip()

    return (startline, headers)


# takes the first line of the request and figures out what the client wants

def parseStartLine(startline):
    parts = startline.split(" ")

    if parts[0] == "POST":
        page, sep, query = parts[1].partition("?")
        querydict = None
        ext = None
        if not sep == "":
            querydict = {}
            for item in query.split("&"):
                field, value = item.split("=")
                querydict[field] = value
        return (page, querydict)

    else:
        print("ERROR - Invalid method : |{0}|".format(parts[0]))
        return None


def recvFullMessage(socket):
    buf = socket.recv(2048)
    if buf == b'':
        return (b'', None, None)
    head, sep, data = buf.partition("\r\n\r\n".encode("utf-8"))
    while not sep:
        buf = buf + socket.recv(2048)
        head, sep, data = buf.partition("\r\n\r\n".encode("utf-8"))

    startline, headers = parseRequest(head.decode("utf-8"))
    if "Content-Length" in headers:
        while len(data) < int(headers["Content-Length"]):
            data = data + socket.recv(2048)

    return (startline, headers, data.decode("utf-8"))


def sendFullMessage(socket, message):
    sent = 0
    while sent < len(message):
        sent = sent + socket.send(message)


def getResponseHead(headers, code="200", data=None):
    if code == "200":
        message = "OK"
    elif code == "404":
        message = "ERROR"

    http = "HTTP/1.1 {0} {1}\r\n".format(code, message)

    if data != None and not "Content-Length" in headers:
        headers["Content-Length"] = len(data)

    for key in headers:
        http = http + "{0}: {1}\r\n".format(key, headers[key])
    http = http + "\r\n"

    if data != None:
        http = http + data

    return http


def pageExists(page):
    return os.path.isfile(page)


def getLastModifiedTime(page):
    return os.path.getmtime(page)


def getLastModifiedTimeFormatted(page):
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(os.path.getmtime(page)))


def parseTimeToSecs(timestamp):
    return strptime(timestamp, "%a, %d %b %Y %H:%M:%S GMT")


# main loop
def printHeaders(headers):
    for header in headers:
        print("{0} : {1}".format(header, headers[header]))


def processAcceptLanguage(al):
    al = "".join(al.split())
    langs = al.split(",")
    langdict = {}
    for lang in langs:
        lan, sep, qual = lang.partition(";q=")
        if sep != "":
            langdict[lan] = float(qual)
        else:
            langdict[lan] = 1
    return langdict

'''
while True:
    try:
        # size of reply message
        size = 0
        # whether the requested file was found
        status = 0

        connectionSocket, addr = serverSocket.accept()
        print("Connection from %s port %s" % addr)
        # Receive the client packet
        startline, headers, data = recvFullMessage(connectionSocket)
        print("Original message : \n" + startline)
        printHeaders(headers)

        # now contains the uri of the file
        page, ext, querydict = parseStartLine(startline)

        if page == "":
            page = "index.html"
        elif page == "favicon.ico":
            page = "factorio.ico"

        # if not found don't try anything else
        if not pageExists(page):
            status = 404
        else:
            status = 200
            if "Accept-Language" in headers and ext == "html":
                preferred = processAcceptLanguage(headers["Accept-Language"])
                for lang in preferred:
                    if pageExists(page + "." + lang):
                        page = page + "." + lang
                        break

            if "If-Modified-Since" in headers:
                if parseTimeToSecs(headers["If-Modified-Since"]) > getLastModifiedTime(page):
                    status = 304

        if status == 200:
            mimetype = mimetypes[ext]

            theFile = open(page, 'r')
            reply = theFile.read()
            size = os.path.getsize(page)
            theFile.close()

            headers = {}
            headers["Content-Length"] = size
            headers["Content-Type"] = mimetype
            headers["Last-Modified"] = getLastModifiedTimeFormatted(page)
            http = getResponseHead(headers, data=reply)

        elif status == 404:
            theFile = open("fnf.html", 'r')
            reply = theFile.read()
            size = os.path.getsize("fnf.html")
            theFile.close()

            headers = {}
            headers["Content-Length"] = size
            headers["Content-Type"] = "text/html"
            headers["Last-Modified"] = getLastModifiedTimeFormatted("fnf.html")
            http = getResponseHead(headers, code="404", message="File Not Found", data=reply)

        elif status == 304:
            headers = {}
            http = getResponseHead(headers, code="304", message="Not Modified")

        if size < 1000:
            print("\n~~~~reply: ")
            print(http)
        else:
            print("Sending an image...")

        sendFullMessage(connectionSocket, http)

        connectionSocket.close()
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break
        # except Exception:
        # print "Something went wrong"
serverSocket.shutdown(SHUT_WR)
serverSocket.close()
'''