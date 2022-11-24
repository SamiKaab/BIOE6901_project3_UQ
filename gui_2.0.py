from time import time
from tkinter import *

from matplotlib import image
# from tomlkit import datetime
import cam
import PIL.Image, PIL.ImageTk, PIL.ImageOps, PIL.ImageFilter, PIL.ImageDraw,PIL.ImageFont
import datetime as dt

import RPi.GPIO as GPIO
from PiicoDev_VL53L1X import PiicoDev_VL53L1X 
import imageTransfer
import _thread

BUTTON_GPIO_OUT = 0


class window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Clinical 3D Surface Scanner")

        # initialise GUI widgets
        self.bottomFrame = Frame(self.master)
        self.bottomFrame.pack(side = BOTTOM,expand=True,fill=X)

        self.btn0 = Button(self.bottomFrame,text = "START", command=self.start,activebackground='white',
                            width = 10,height = 2,font=('calibri',12,'bold'))
        self.btn0.pack(side=BOTTOM)
        self.laserLabel = Label(self.bottomFrame,width=10)
        self.laserLabel.pack(side = LEFT)

        self.label = Label(self.master)
        self.label.pack(side = TOP, ipadx=2, ipady=2)

        self.master.bind('<Escape>', lambda e: self.close_all())
        self.master.bind('<Return>', lambda e: self.capture())
        self.master.protocol("WM_DELETE_WINDOW", self.close_all)


        self.init_pb()
        self.init_pb_out()
        self.distSensor = PiicoDev_VL53L1X() # create the sensor object
        self.dist = 0
        self.mode = 0 # idle by default, 1 for capture mode


        self.listCamId = ['31704551','31707351','31700851','32702251','32704451','31701451']
        self.listCams = cam.init_all_cams(self.listCamId)

        # self.laser_thread =_thread.start_new_thread( self.show_laser,())
        # self.frame_thread = _thread.start_new_thread( self.show_frame,())
        # self.show_laser()
        self.show_frame()
        
    # update the laser labe to display the current distance read by the distance sensor
    def show_laser(self):
        self.dist = self.distSensor.read()
        self.laserLabel.configure(text = str(self.dist/10)+"cm")#text= dt.datetime.now().time().isoformat())
        self.laserLabel.update()
        # self.laserLabel.after(10,self.show_laser)
        
    # display frame and relevant information 
    def show_frame(self):
        self.show_laser()

        cam.get_frames(self.listCams)
        photo = self.listCams[0][2] #get image from first camera
        photo = photo.get_image_data_numpy()
        photo = PIL.Image.fromarray(photo).convert('RGB')
        x, y = photo.size
        photo = photo.resize((int(x/1.1),int(y/1.1)))
        x, y = photo.size
        r,g,b = photo.split()# blue and red are inverted in photo
        if self.mode == 0: #convert to greyscale
            g=r
            b=r
        photo = PIL.Image.merge('RGB',(b,g,r))
        if self.mode == 0:
            
            photo = photo.filter(PIL.ImageFilter.GaussianBlur(3))
            draw = PIL.ImageDraw.Draw(photo)
  
            # use a truetype font
            font = PIL.ImageFont.truetype("fonts/GROT_L.ttf", 100)
            
            # specifying coordinates and colour of text
            draw.text((x/5,y/3), "Press Start to\n begin scan", (255, 255, 255), font=font)

        elif self.mode == 1: # in capture mode
            draw = PIL.ImageDraw.Draw(photo)
  
            # use a truetype font
            font = PIL.ImageFont.truetype("fonts/GROT_L.ttf", 100)
            if self.dist < 300: #object is too close
                self.label.config(background='red')
                # specifying coordinates and colour of text
                draw.text((x/4,y/3), "Move Back", (255, 255, 255), font=font)
            elif self.dist > 800: # object is too far
                self.label.config(background='red')
                # specifying coordinates and colour of text
                draw.text((x/4,y/3), "Move Closer", (255, 255, 255), font=font)
            else :
                self.label.config(background='green')

        photo = PIL.ImageTk.PhotoImage(image = photo)
        
        self.label.photo = photo
        self.label.configure(image = photo)
        self.label.after(5,self.show_frame) #wait for 5 milliseconds

    # change to capture mode or idle mode based on current state
    def start(self):
        if self.mode == 0:
            print("initialise camera")
            self.btn0.configure(text = "STOP")
            self.mode = 1
            print("in capture mode")
        elif self.mode == 1:
            print("close cameras")
            # cam.close_cameras(self.cam0,self.cam1)
            self.btn0.configure(text = "START")
            self.mode = 0
            print("in Idle mode")
            # Transfer images from auxillary raspberry pi to the main raspberry pi
            imageTransfer.scp("/home/pi/project3/images","/home/pi/project3/","project3","pi","rpi11")
            imageTransfer.scp("/home/pi/project3/images","/home/pi/project3/","project3","pi","rpi13")
            
            self.master.update()

    # initialise input intterupt 
    def init_pb(self):
        BUTTON_GPIO = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=self.button_callback, bouncetime=1000)
    
    # initialise output intterupt 
    def init_pb_out(self):
        BUTTON_GPIO_OUT = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO_OUT, GPIO.OUT)

    # Pushbutton interrupt callback function
    def button_callback(self,channel):
        if self.mode == 1:
            GPIO.output(BUTTON_GPIO_OUT,1)
            imageFileList = cam.save_images(self.listCams)
            print("image saved")
            GPIO.output(BUTTON_GPIO_OUT,0)
    
    def capture(self):
        if self.mode == 1:
            cam.save_images(self.listCams)
            print("capture")

    def close_all(self):
        # _thread.exit()
        cam.close_cameras(self.listCams)
        GPIO.output(BUTTON_GPIO_OUT,0)
        GPIO.cleanup()
        self.master.quit()



if __name__ == "__main__":
    root = Tk()
    app = window(root)
    root.mainloop()
