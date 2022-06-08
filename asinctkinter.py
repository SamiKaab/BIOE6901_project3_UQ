import asyncio
import tkinter as tk

from async_tkinter_loop import async_mainloop, async_handler

class window(object):
    def __init__(self,master = None):
        self.master = None
        self.label = tk.Label(root)
        self.label.pack()

        tk.Button(root, text="Start", command=async_handler(self.counter)).pack()

    async def counter(self):
        i = 0
        while True:
            i += 1
            self.label['text'] = str(i)
            await asyncio.sleep(1.0)


root = tk.Tk()

app = window(root)

async_mainloop(root)