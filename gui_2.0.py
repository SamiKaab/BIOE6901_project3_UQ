from tkinter import *

from matplotlib import image
import cam
import PIL.Image, PIL.ImageTk, PIL.ImageOps, PIL.ImageFilter, PIL.ImageDraw,PIL.ImageFont



class window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.btn0 = Button(self.master,text = "start", command=self.start)
        self.btn0.pack(side=BOTTOM)

        self.label = Label(self.master)
        self.label.pack(side = TOP)
        
        self.count = 0
        self.mode = 0 # idle by default, 1 for capture mode

        self.master.bind('<Escape>', lambda e: self.close_all())
        self.master.protocol("WM_DELETE_WINDOW", self.close_all)
        
        self.listCamId = ['32704451','32702251','31702051','31707351',]
        self.listCams = cam.init_all_cams(self.listCamId)
        self.show_frame()
        
        
    
        
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

    def close_all(self):
        cam.close_cameras(self.listCams)
        self.master.quit()



if __name__ == "__main__":
    root = Tk()
    app = window(root)
    root.mainloop()