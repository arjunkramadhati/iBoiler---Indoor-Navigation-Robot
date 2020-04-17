from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as font
import guibuilder as gui

'''
1. Import all the necessary libraries. (Have all the libraries above.)
2. Place your map image file in the current directory you are running pythons codes.
(i.e. if your pythons codes are placed in C:/Users/Desktop/CNIT581/Project, 
place the image file in the exact same directory.)
You can call the gui window by passing map image as an argument.
'''

gui.Window(mapImage="map.jpg")