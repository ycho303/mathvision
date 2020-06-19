from tkinter import *
from PIL import ImageTk, Image
import numpy as np

def get_y(x, a, b, c, d):
    return a * np.sin(b * x + c) + d

def jacobian(x, a, b, c, d):
    return [-np.sin(b * x + c), -a * x * np.cos(b * x + c), -a * np.cos(b * x + c), -1]

def compatable_img(img):
    return ImageTk.PhotoImage(img)

class MainWindow():

    def __init__(self, main):        
        background = Image.open('./canvas.jpg')
        self.w, h = background.size

        self.canvas = Canvas(main, width=self.w, height=h)
        self.canvas.grid(row=0, column=1)

        self.my_image = compatable_img(background)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.my_image)

        self.x = []
        self.y = []
        self.plot = None
        
    def clear(self):
        global processed
        processed = False
        self.canvas.delete('all')
        self.x = []
        self.y = []
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.my_image)

    def draw_pt(self, x, y):
        if not processed:
            self.x.append(x)
            self.y.append(y)
            self.canvas.create_circle(x, y, 3, fill="white")
        else:
            print('Press "c" to restart')

    def plot_sine(self, p):
        self.canvas.delete(self.plot)
        x = np.linspace(0, self.w, self.w)
        func_y = np.array([get_y(x, *p) for x in x])
        self.plot = self.canvas.create_line([(x, y) for x, y in zip(x, func_y)], fill='green')

    def delta_p(self, p_, p):
        return np.linalg.norm(np.absolute(p_-p))

    def fit(self):
        global processed
        processed = True
        self.x = np.array(self.x)
        self.y = np.array(self.y)
        term_max_iter = 1000
        term_tolerance = 1e-10
        p = [np.std(self.y), 0.01, 40, np.mean(self.y)]

        for i in range(term_max_iter):
            func_y = np.array([get_y(x, *p) for x in self.x])

            r = self.y - func_y
            j = np.vstack([jacobian(x, *p) for x in self.x])
            p_ = np.array(p) - np.linalg.inv(j.T @ j) @ j.T @ r

            if self.delta_p(p_, p) < term_tolerance:
                print(f'break at iter: {i}')
                break

            p = p_
            self.plot_sine(p)

event_x, event_y = 0, 0
processed = False

def detectMotion(event):
    global event_x, event_y
    event_x, event_y = event.x, event.y

def drawOnLeftClick(event):
    model.draw_pt(event_x, event_y)

def clear(event):
    model.clear()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def submit(event):
    model.fit()

import tkinter as tk
tk.Canvas.create_circle = _create_circle
root = Tk()
root.title('Sine Fitting')
model = MainWindow(root)
root.bind('<Motion>', detectMotion)
root.bind("<Button-1>", drawOnLeftClick)
root.bind("c", clear)
root.bind('<Return>', submit)
root.mainloop()