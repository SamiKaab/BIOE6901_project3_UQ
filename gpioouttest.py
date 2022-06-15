import RPi.GPIO as GPIO
import time
BUTTON_GPIO = 0

def init_pb_out():
    BUTTON_GPIO = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.OUT)

init_pb_out()
try:
    while True:
        GPIO.output(BUTTON_GPIO,1)
        time.sleep(1)
        GPIO.output(BUTTON_GPIO,0)
        time.sleep(1)
except:
    GPIO.output(BUTTON_GPIO,0)
    GPIO.cleanup()
    print("bye")
