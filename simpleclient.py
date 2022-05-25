import base64
import socket
from time import sleep
from time import time
import cv2 as cv
import numpy as np
# cv.imshow("test", pic)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

host = '192.168.0.4'
port = 5560

def sendPic(s, filePath,fileName):
    print(filePath)
    # pic = open(filePath, 'rb')
    pic = cv.imread(filePath,cv.IMREAD_COLOR)
    pic = cv.resize(pic,dsize=(480,315))

    encode_param = [int(cv.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv.imencode('.jpg',pic, encode_param)
    data = np.array(imgencode)
    stringData = base64.b64encode(data)
    length = str(len(stringData))
    s.sendall(fileName.encode('utf-8').ljust(64))
    s.sendall(length.encode('utf-8').ljust(64))
    s.send(stringData)

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

s = setupSocket()

filePath = '/home/pi/project3/img0.png'

sendPic(s, filePath,"img0")
filePath = '/home/pi/project3/img1.png'

sendPic(s, filePath,"img1")


s.close()
