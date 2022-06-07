from tkinter import *

from matplotlib import image
import cam
import PIL.Image, PIL.ImageTk, PIL.ImageOps



class window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        btn0 = Button(self.master,text = "start", command=self.sayHi)
        btn0.pack(side=BOTTOM)

        self.label = Label(self.master)
        self.label.pack(side = TOP)

        self.master.bind('<Escape>', lambda e: self.close_all())
        self.master.protocol("WM_DELETE_WINDOW", self.close_all)

        self.cam0,self.cam1,self.img0,self.img1 = cam.init_cam()
        self.show_frame()
        
    
        
    def show_frame(self):
        self.cam0.get_image(self.img0)
        self.cam1.get_image(self.img1)
        photo = PIL.Image.fromarray(self.img0.get_image_data_numpy()).convert('RGB')
        r,g,b = photo.split()
        photo = PIL.Image.merge('RGB',(b,g,r))
        photo = PIL.ImageTk.PhotoImage(image = photo)
        self.label.photo = photo
        self.label.configure(image = photo)
        self.label.after(5,self.show_frame)

    def sayHi(self):
        print("hi")

    def close_all(self):
        cam.close_cameras(self.cam0,self.cam1)
        self.master.quit()



if __name__ == "__main__":
    root = Tk()
    app = window(root)
    root.mainloop()