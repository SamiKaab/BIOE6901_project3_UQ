# from asyncio.windows_events import NULL
import cam
import cv2 as cv
import simpleServer
import simpleClient
import time
import RPi.GPIO as GPIO

def init_pb():
    BUTTON_GPIO = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback, bouncetime=1000)


def button_callback(channel):

    img0_name, img1_name, img0_file_path, img1_file_path = cam.save_images(cam0, cam1,img0, img1)
    print("image saved")
    simpleClient.sendPic(s, img0_file_path, img0_name)  #client
    simpleClient.sendPic(s, img1_file_path, img1_name)  #client
    print("image sent")

  

def main():
    init_pb()
    global s
    s = simpleClient.setupSocket()          #client

    global cam0,cam1,img0,img1
    cam0,cam1,img0,img1 = cam.init_cam()


    try:
        while True:
            # cam0.get_image(img0)
            # cam1.get_image(img1)
            # cv.imshow("Output",img0.get_image_data_numpy())
            # cv.imshow("Output2",img1.get_image_data_numpy())
            # cv.waitKey(1)
            # # if (c == ord(' ')):
                        
            # #     cv.imwrite("cam0_" + str(dn) + ".png", img0.get_image_data_numpy())
            # #     cv.imwrite("cam1_" + str(dn) + ".png", img1.get_image_data_numpy())
            continue
            
    except:
        cam.close_cameras(cam0,cam1)
        s.close()
        GPIO.cleanup()

main()
