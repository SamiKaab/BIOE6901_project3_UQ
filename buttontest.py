# import time
# import RPi.GPIO as GPIO
# BUTTON_GPIO = 16

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# pressed = False

# def triggered(channel):
#     print("hi")

# GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback = triggered, bouncetime = 50)

# try:
#     while True:
#         pass
# except:
#     GPIO.cleanup()

import signal                   
import sys
import RPi.GPIO as GPIO
BUTTON_GPIO = 16
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_callback(channel):
    print("Button pressed!")
  

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback, bouncetime=500)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()