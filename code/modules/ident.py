import matplotlib.pylab as plt
import numpy as np
import os

class Identifier():
    def __init__(self, ax):
        self.ax = ax
        self.x_stack = []
        self.y_stack = []
        self.counter = 0
        self.tx_stack = []
        self.shift_is_held = False
        self.text = self.ax.text(0 , 1 ,'', transform = self.ax.transAxes)
        self.shift_text = self.ax.text(0 , 1.1,self.shift_is_held,transform = self.ax.transAxes)

    def onclick(self,event):
        if self.shift_is_held != False:
            self.counter += 1
            tx = '%d-th Click:xdata=%f, ydata=%f' % (self.counter, event.xdata, event.ydata)
            self.tx_stack.append(tx)
            self.text.set_text(tx)
            self.x_stack.append(event.xdata)
            self.y_stack.append(event.ydata)
            self.ax.plot(event.xdata, event.ydata,'bo',ms = 4)
            self.ax.figure.canvas.draw()

    def undo(self, event):
        if event.key == 'u' and self.counter >=1:
            self.counter -= 1
            self.x_stack.pop()
            self.y_stack.pop()
            self.tx_stack.pop()
            if self.counter >1:
                self.text.set_text(self.tx_stack[-1])
            else:
                self.text.set_text("")
            self.ax.lines.pop()
            self.ax.figure.canvas.draw()

    def on_toggle(self, event):
        if event.key == 'shift':
            self.shift_is_held = True
            self.shift_text.set_text(True)
            self.ax.figure.canvas.draw()

    def off_toggle(self, event):
        if event.key == 'shift':
            self.shift_is_held = False
            self.shift_text.set_text(False)
            self.ax.figure.canvas.draw()
            
    def disconnect(self,event):
        if event.key == 'c':
            self.ax.figure.canvas.mpl_disconnect(self.cid_undo)
            self.ax.figure.canvas.mpl_disconnect(self.cid_click)
            self.ax.figure.canvas.mpl_disconnect(self.cid_shift_on)
            self.ax.figure.canvas.mpl_disconnect(self.cid_shift_off)
            self.export()

    def connect(self):
        self.cid_click = self.ax.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid_undo = self.ax.figure.canvas.mpl_connect('key_press_event', self.undo)
        self.cid_disconnect = self.ax.figure.canvas.mpl_connect('key_press_event', self.disconnect)
        self.cid_shift_on = self.ax.figure.canvas.mpl_connect('key_press_event', self.on_toggle)
        self.cid_shoft_off = self.ax.figure.canvas.mpl_connect('key_release_event', self.off_toggle)

    def export(self):
        return np.array([self.x_stack,self.y_stack]).transpose()
