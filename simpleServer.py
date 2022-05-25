import socket
import cv2 as cv
import numpy as np
import base64
# from cookieLED import callLED

host = ''
port = 5560

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s

def setupConnection():
    s.listen(True) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def getImage(conn):
    #Visualize the received data
    fileName = recvall(conn,64)
    if fileName:
        length = recvall(conn,64)
        length = length.decode('utf-8')
        stringData = recvall(conn, int(length))
        data = np.frombuffer(base64.b64decode(stringData), np.uint8)
        decimg = cv.imdecode(data, 1)
        # cv.imshow("image", decimg)
        print("done")
        cv.imwrite("images/{}.png".format(fileName.decode('utf-8').split(' ')[0]), decimg)
        return 1
    else:
        return 0


s = setupServer()
conn = setupConnection()
while True:
    if not getImage(conn):
        break
    
s.close()