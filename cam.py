
from pickle import TRUE
import cv2 as cv
from ximea import xiapi
import time
import datetime as dt
import sys
import signal                   
import RPi.GPIO as GPIO



def init_cam():
    #create instance for first connected camera
    
    cam0 = xiapi.Camera()
    cam1 = xiapi.Camera()


    #start communication
    #to open specific device, use:
    cam0.open_device_by_SN('31707351') #('31702051') #()
    cam0.set_imgdataformat('XI_RGB24')
    cam0.disable_auto_wb()

    cam1.open_device_by_SN('31701451') #('32704451')
    cam1.set_imgdataformat('XI_RGB24')
    cam1.disable_auto_wb()
    #(open by serial number)
    print('Opening first camera...')
    # cam0.open_device()

    #settings
    cam0.set_exposure(10000)
    cam1.set_exposure(10000)
    # print('Exposure was set to %i us' %cam0.get_exposure())
    #start data acquisition
    print('Starting data acquisition...')
    cam0.start_acquisition()
    cam1.start_acquisition()
    #create instance of Image to store image data and metadata
    img0 = xiapi.Image()
    img1 = xiapi.Image()

    return cam0,cam1,img0,img1


def save_images(cam0, cam1, img0, img1):
    cam0.get_image(img0)
    cam1.get_image(img1)
    dn = dt.datetime.now()
    t = dn.time()
    tformated = str(t.hour) + "-" + str(t.minute) + "-" + str(t.second) + "-" + str(t.microsecond)
    f = str(dn.date().isoformat())
    img0_name = str(f) + "_" + str(tformated) + "_RPi3_cam0.png" 
    img1_name = str(f) + "_" + str(tformated) + "_RPi3_cam1.png" 
    img0_file_path = "images/" + img0_name
    img1_file_path = "images/" + img1_name    
    cv.imwrite(img0_file_path, img0.get_image_data_numpy())
    cv.imwrite(img1_file_path, img1.get_image_data_numpy())  
    return [img0_name, img1_name, img0_file_path, img1_file_path]

def close_cameras(cam0,cam1):
    #stop data acquisition
    print('Stopping acquisition...')
    cam0.stop_acquisition()
    cam1.stop_acquisition()

    #stop communication
    cam0.close_device()
    cam1.close_device()
