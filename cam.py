
from pickle import TRUE
import cv2 as cv
from ximea import xiapi
import time
import datetime as dt
import sys
import signal                   
import RPi.GPIO as GPIO


def button_callback(channel):
    dn = dt.datetime.now()
    # f = dn.year + dn.month + dn.day + dn.time()
    
    cv.imwrite("cam0_" + str(dn) + ".png", img0.get_image_data_numpy())
    cv.imwrite("cam1_" + str(dn) + ".png", img1.get_image_data_numpy())
            
    print("Button pressed!")



def init_cam():
    #create instance for first connected camera
    cam0 = xiapi.Camera()
    cam2 = xiapi.Camera()


    #start communication
    #to open specific device, use:
    cam0.open_device_by_SN('31707351')
    cam0.set_imgdataformat('XI_RGB24')
    cam0.disable_auto_wb()

    cam2.open_device_by_SN('31701451')
    cam2.set_imgdataformat('XI_RGB24')
    cam2.disable_auto_wb()
    #(open by serial number)
    print('Opening first camera...')
    # cam0.open_device()

    #settings
    cam0.set_exposure(10000)
    cam2.set_exposure(10000)
    print('Exposure was set to %i us' %cam0.get_exposure())
    #start data acquisition
    print('Starting data acquisition...')
    cam0.start_acquisition()
    cam2.start_acquisition()
    #create instance of Image to store image data and metadata
    img0 = xiapi.Image()
    img1 = xiapi.Image()

    return cam0,cam2,img0,img1


def init_pb():
    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback, bouncetime=1000)


init_pb()
cam0,cam2,img0,img1 = init_cam()



try:
    while True:
        cam0.get_image(img0)
        cam2.get_image(img1)
        cv.imshow("Output",img0.get_image_data_numpy())
        cv.imshow("Output2",img1.get_image_data_numpy())
        cv.waitKey(1)
        # if (c == ord(' ')):
                    
        #     cv.imwrite("cam0_" + str(dn) + ".png", img0.get_image_data_numpy())
        #     cv.imwrite("cam1_" + str(dn) + ".png", img1.get_image_data_numpy())
        
except:
    #stop data acquisition
    print('Stopping acquisition...')
    cam0.stop_acquisition()
    cam2.stop_acquisition()

    #stop communication
    cam0.close_device()
    cam2.close_device()

    GPIO.cleanup()
