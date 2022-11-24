__author__ = "Sami Kaab"
#__copyright__ = ""
#__credits__ = [""]
#__license__ = "GPL"
__version__ = "1.2"
#__maintainer__ = ""
__email__ = "sami.kaab@outlook.com"
__status__ = "In Development"

import cam
import cv2 as cv
import time
import RPi.GPIO as GPIO

# initialise push button interrupt
def init_pb():
    BUTTON_GPIO = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback, bouncetime=1000)


# pushbutton interrupt call back function
def button_callback(channel):
    cam.save_images(listCams)
    print("image saved")
    
def main():
    init_pb()

    listCamId = ['32704451','32702251','31702051','31707351',]
    global listCams
    listCams = cam.init_all_cams(listCamId)

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
        cam.close_cameras(listCams)
        GPIO.cleanup()

main()
