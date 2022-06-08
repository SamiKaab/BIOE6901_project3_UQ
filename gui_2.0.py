from time import time
from tkinter import *

from matplotlib import image
from tomlkit import datetime
import cam
import PIL.Image, PIL.ImageTk, PIL.ImageOps, PIL.ImageFilter, PIL.ImageDraw,PIL.ImageFont
import datetime as dt

# import RPi.GPIO as GPIO
# from PiicoDev_VL53L1X import PiicoDev_VL53L1X 
import _thread




class window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
       
        self.bottomFrame = Frame(self.master)
        self.bottomFrame.pack(side = BOTTOM,expand=True,fill=X)

        self.btn0 = Button(self.bottomFrame,text = "start", command=self.start)
        self.btn0.pack(side=BOTTOM)
        self.laserLabel = Label(self.bottomFrame)
        self.laserLabel.pack(side = LEFT)

        self.label = Label(self.master)
        self.label.pack(side = TOP)

        
        self.count = 0
        self.mode = 0 # idle by default, 1 for capture mode

        self.master.bind('<Escape>', lambda e: self.close_all())
        self.master.bind('<Return>', lambda e: self.capture())
        self.master.protocol("WM_DELETE_WINDOW", self.close_all)

        # self.init_pb()
        # self.distSensor = PiicoDev_VL53L1X() # create the sensor object


        self.listCamId = ['32704451','32702251','31702051','31707351',]
        self.listCams = cam.init_all_cams(self.listCamId)

        _thread.start_new_thread( self.show_laser,())
        _thread.start_new_thread( self.show_frame,())
        
        
    
    def show_laser(self):
        dist = self.count#self.distSensor.read()
        self.laserLabel.configure(text= dt.datetime.now().time().isoformat())
        self.count+=1
        self.laserLabel.after(5,self.show_laser)


        
    def show_frame(self):
        self.label.configure(text = "video here {}".format(self.count))
        self.count+=1

        cam.get_frames(self.listCams)
        photo = self.listCams[0][2]
        photo = photo.get_image_data_numpy()
        photo = PIL.Image.fromarray(photo).convert('RGB')
        x, y = photo.size
        r,g,b = photo.split()
        if self.mode == 0:
            g=r
            b=r
        photo = PIL.Image.merge('RGB',(b,g,r))
        if self.mode == 0:
            
            photo = photo.filter(PIL.ImageFilter.BLUR)
            photo = photo.filter(PIL.ImageFilter.BLUR)
            photo = photo.filter(PIL.ImageFilter.BLUR)
            draw = PIL.ImageDraw.Draw(photo)

  
            # use a truetype font
            font = PIL.ImageFont.truetype("fonts/GROT_L.ttf", 100)
            
            # specifying coordinates and colour of text
            
            draw.text((x/3.5,y/3), "Press Start to\n begin scan", (255, 255, 255), font=font)

            
       

        photo = PIL.ImageTk.PhotoImage(image = photo)
        
        self.label.photo = photo
        self.label.configure(image = photo)
        self.label.after(5,self.show_frame)
        # if self.mode == 1:
        #     self.label.configure(text = "Press Start to begin scan", font=("Helvetica", 18))

    def start(self):
        if self.mode == 0:
            print("initialise camera")
            
            self.btn0.configure(text = "stop")
            self.mode = 1
            print("in capture mode")
        elif self.mode == 1:
            print("close cameras")
            # cam.close_cameras(self.cam0,self.cam1)
            self.btn0.configure(text = "start")
            self.mode = 0
            print("in Idle mode")
            
            self.master.update()

    # def init_pb(self):
    #     BUTTON_GPIO = 26
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
    #     GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=self.button_callback, bouncetime=1000)


    # def button_callback(self,channel):
    #     if self.mode == 1:
    #         imageFileList = cam.save_images(self.listCams)
    #         print("image saved")
    
    def capture(self):
        if self.mode == 1:
            cam.save_images(self.listCams)
            print("capture")

    def close_all(self):
        cam.close_cameras(self.listCams)
        self.master.quit()



if __name__ == "__main__":
    root = Tk()
    app = window(root)
    root.mainloop()