import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, filedialog, Label #, Style, BOTH, Frame #themed tk
from PIL import ImageTk, Image
from skimage import io, data, filters, exposure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana", 12)
class Base(tk.Tk):

    def __init__(self):
        #Configurations
        tk.Tk.__init__(self) #Initializes object window

        #self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='/home/mx/github/PSOCVIS/Pictures-icon.png'))
        tk.Tk.wm_title(self,"Chan-Vese algorithm PSO solved image segmentation")
        container = tk.Frame(self) #A frame to fill with widgets
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1) #min value and priority config
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(container) #Menu bar root frame
        #menu items
        file_menu = Menu(menu_bar, tearoff=0)#
        file_menu.add_command(label="New")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save As...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)#
        menu_bar.add_cascade(label="File",menu=file_menu)
        
        edit_menu = Menu(menu_bar, tearoff=0)
        
        sub_menu = Menu(edit_menu, tearoff=0)
        sub_menu.add_command(label = "Load", command=self.load_image)
        sub_menu.add_command(label = "Otsu's Transformation", command=self.Otsu_seg)
        edit_menu.add_cascade(label = "Image", menu = sub_menu)
        
        edit_menu.add_separator()
        edit_menu.add_command(label="Parameters", command=quit)
        menu_bar.add_cascade(label="Edit",menu=edit_menu)
        tk.Tk.config(self,menu = menu_bar) # Display menu bar
        #Window container
        self.frames = {} #All frames same app
        for F in (StartPage, Parameters):
        #Window container assignation
            frame = F(container, self) #First of all frames
            self.frames[F] = frame #Configured StartPage stored on dict.
            frame.grid(row = 0, column = 0, sticky="nsew") #Optimized Org. central cardinality
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #Show upfront
    def load_image(self):
        self.address = filedialog.askopenfilename(initialdir="/home/mx/github/PSOCVIS",
        title="Select an image", filetypes=(("png files","*.png"),("all files","*.*")))
        
        mImage = io.imread(self.address, as_gray=True)
        #io.imshow(mImage)
        fig = Figure(figsize=(5, 5), dpi=100)
        a = fig.add_subplot(111)
        a.matshow(mImage)
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def Otsu_seg(self):
        camera = data.imread("CPM3.jpg", as_gray=True) #returns size
        val = filters.threshold_otsu(camera)
        hist, bins_center = exposure.histogram(camera)
        fig = Figure(figsize=(9, 4), dpi=100)
        fig.add_subplot(131)
        io.imshow(camera, cmap='gray', interpolation='nearest')
        #fig.axis('off')
        fig.add_subplot(132)
        io.imshow(camera < val, cmap='gray', interpolation='nearest')
        #fig.axis('off')
        fig.add_subplot(133)
        plt.plot(bins_center, hist, lw=2)
        plt.axvline(val, color='k', ls='--')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
'''
class Otsu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Segmentación metodo Otsu", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        camera = data.imread("CPM3.jpg", as_gray=True) #returns size
        val = filters.threshold_otsu(camera)
        hist, bins_center = exposure.histogram(camera)
        fig = Figure(figsize=(9, 4), dpi=100)
        fig.add_subplot(131)
        io.imshow(camera, cmap='gray', interpolation='nearest')
        #fig.axis('off')
        fig.add_subplot(132)
        io.imshow(camera < val, cmap='gray', interpolation='nearest')
        #fig.axis('off')
        fig.add_subplot(133)
        plt.plot(bins_center, hist, lw=2)
        plt.axvline(val, color='k', ls='--')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
'''
class Parameters(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Parameters", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

app = Base()
app.geometry("1280x720")
app.mainloop()
'''
mImage = io.imread("Max_contrast_Brain_MRI_131058_rgbcb.png", as_gray=True)
print(mImage)
plt.imshow(mImage)
plt.colorbar()

m1Image = io.imread("Max_contrast_Brain_MRI_131058_rgbcb.png", as_gray=True)
print(m1Image)
plt.imshow(m1Image)

m2Image = io.imread("CPM3.jpg", as_gray=True)
print(m2Image)
plt.imshow(m2Image)
plt.colorbar()
'''