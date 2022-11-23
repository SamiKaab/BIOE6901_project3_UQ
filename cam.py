
from pickle import TRUE
import cv2 as cv
from ximea import xiapi
import time
import datetime as dt
import sys
import signal                   
# import RPi.GPIO as GPIO



def init_cam(camID):
    #create instance for first connected camera
    
    cam = xiapi.Camera()


    #start communication
    #to open specific device, use:
    cam.open_device_by_SN(camID)#.('31702051')#('31707351')#
    cam.set_imgdataformat('XI_RGB24')
    cam.disable_auto_wb()

    
    #(open by serial number)
    print('Opening first camera...')
    # cam0.open_device()

    #settings
    cam.set_exposure(10000)
    # print('Exposure was set to %i us' %cam0.get_exposure())
    #start data acquisition
    print('Starting data acquisition...')
    cam.start_acquisition()
    #create instance of Image to store image data and metadata
    img = xiapi.Image()

    return cam,img


def save_images(listCams):
    imageFileList = []
    for camInfo in  listCams:
        id = camInfo[0]
        cam = camInfo[1]
        img = camInfo[2]
        cam.get_image(img)
        # get date/time info
        dn = dt.datetime.now()
        t = dn.time()
        tformated = str(t.hour) + "-" + str(t.minute) + "-" + str(t.second) + "-" + str(t.microsecond)
        f = str(dn.date().isoformat())
        # set name
        img_name = str(f) + "_" + str(tformated) + "_RPi3_cam"+str(id)+".png" 
        img_file_path = "images/" + img_name
        # save image
        cv.imwrite(img_file_path, img.get_image_data_numpy())
        imageFileList.append([img_name, img_file_path])
    return imageFileList

def close_cameras(listCams):
    print('Stopping acquisition...')
    for id, cam,img in listCams:
        #stop data acquisition
        cam.stop_acquisition()

        #stop communication
        cam.close_device()

def init_all_cams(listCamId):
    listCams = []
    for id in listCamId:
        try:
            cam,img = init_cam(id)
            listCams.append([id,cam,img])
        except:
            print(id+" failed init")
            continue
    return listCams


def get_frames(listCams):
    i = 0
    for camInfo in  listCams:
        id = camInfo[0]
        cam = camInfo[1]
        img = camInfo[2]
        cam.get_image(img)
        listCams[i][2] = img
        i+=1
        
        
    

if __name__ == "__main__":
    listCamId = ['32704451','32702251','31702051','31707351',]
    listCams = init_all_cams(listCamId)

    
    try:
        while True:
            get_frames(listCams)
            cv.imshow(listCamId[0], listCams[0][2].get_image_data_numpy())
            cv.waitKey(1)
                
    except:
        close_cameras(listCams)