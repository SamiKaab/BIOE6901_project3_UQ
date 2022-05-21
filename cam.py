
from pickle import TRUE
import cv2 as cv
from ximea import xiapi
import time
import sys
import signal                   
import RPi.GPIO as GPIO

idx = 0

def button_callback(channel):
    global idx 

    cv.imwrite("cam_img_" + str(idx) + ".png", img.get_image_data_numpy())
    cv.imwrite("cam2_img_" + str(idx) + ".png", img2.get_image_data_numpy())
    idx = idx + 1
            
    print("Button pressed!")



def init_cam():
    
    #create instance for first connected camera
    cam = xiapi.Camera()
    cam2 = xiapi.Camera()


    #start communication
    #to open specific device, use:
    cam.open_device_by_SN('31707351')
    cam.set_imgdataformat('XI_RGB24')
    cam.disable_auto_wb()

    cam2.open_device_by_SN('31701451')
    cam2.set_imgdataformat('XI_RGB24')
    cam2.disable_auto_wb()
    #(open by serial number)
    print('Opening first camera...')
    # cam.open_device()

    #settings
    cam.set_exposure(10000)
    cam2.set_exposure(10000)
    print('Exposure was set to %i us' %cam.get_exposure())
    #start data acquisition
    print('Starting data acquisition...')
    cam.start_acquisition()
    cam2.start_acquisition()
    #create instance of Image to store image data and metadata
    img = xiapi.Image()
    img2 = xiapi.Image()

    return cam,cam2,img,img2

def init_pb():
    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback, bouncetime=1000)



init_pb()
cam,cam2,img,img2 = init_cam()




try:
    while True:
        cam.get_image(img)
        cam2.get_image(img2)
        cv.imshow("Output",img.get_image_data_numpy())
        cv.imshow("Output2",img2.get_image_data_numpy())
        c = cv.waitKey(1)
        if (c == ord(' ')):
            cv.imwrite("cam_img_" + str(idx) + ".png", img.get_image_data_numpy())
            cv.imwrite("cam2_img_" + str(idx) + ".png", img2.get_image_data_numpy())
            idx += 1
        
except:
    #stop data acquisition
    print('Stopping acquisition...')
    cam.stop_acquisition()
    cam2.stop_acquisition()

    #stop communication
    cam.close_device()
    cam2.close_device()

    GPIO.cleanup()