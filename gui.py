from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as font
from databaseManager import databaseManager
import matplotlib
from iBoilerTry import iBoiler
import cv2
import threading
import time
import PIL.Image, PIL.ImageTk
import numpy as np

class gui(Frame):

    def __init__(self):

        master = Tk()
        Frame.__init__(self, master)

        self.dbHelper = databaseManager('Database/db')
        self.iBoilerObj = iBoiler('physics_corrected.jpg','Database/db',4,5,5,10,4.32,3.18,0.7,1)
        self.canvasMapBig = Canvas(master,width=650, height=900 ,bg="gray")
        self.canvasMapBig.place(x=10,y=10)
        self.canvasMapZoom = Canvas(master,width=900, height=900 ,bg="gray")
        self.canvasMapZoom.place(x=1500,y=10)

        
        self.startListName = Label(master, text = "Enter pick-up room number" )
        self.startListName.place(x= 700, y = 50)
        self.startListName['font'] = font.Font(size = 30)
        self.startList = list(self.dbHelper.getDbEntry('L4').keys())
        self.goalList = list(self.dbHelper.getDbEntry('L4').keys())
        self.startListSelected = StringVar(master)
        self.startListSelected.set(self.startList[0])

        startOptionMenu = OptionMenu(master,self.startListSelected, *self.startList,command=self.setStartNumber)
        startOptionMenu['font'] = font.Font(size= 25)
        startOptionMenu.place(x=730, y = 100)

        self.goalListName = Label(master, text = "Enter drop-off room number" )
        self.goalListName.place(x= 700, y = 250)
        self.goalListName['font'] = font.Font(size = 30)
        #self.goalList = list(self.dbHelper.getDbEntry('L4').keys())
        
        self.goalListSelected = StringVar(master)
        self.goalListSelected.set(self.goalList[0])

        goalOptionMenu = OptionMenu(master,self.goalListSelected, *self.goalList, command=self.setGoalNumber)
        goalOptionMenu['font'] = font.Font(size= 25)
        goalOptionMenu.place(x=730, y = 300)

        buttonStartOperations = Button(master, text = "Begin Simulation" )
        buttonStartOperations['font'] = font.Font(size = 30)
        buttonStopOperations = Button(master, text = "Halt Simulation" )
        buttonStopOperations['font'] = font.Font(size = 30)
        buttonResetOperations = Button(master, text = "Reset Simulation" )
        buttonResetOperations['font'] = font.Font(size = 30)

        buttonStartOperations.place(x= 700, y = 400)
        buttonStopOperations.place(x=700,y=500)
        buttonResetOperations.place(x=700, y=600)

        buttonStartOperations.bind("<Button-1>",self.startOperations)
        buttonStopOperations.bind("<Button-1>",self.stopOperations)

        master.wm_title("iBoiler Simulation")
        master.geometry("2500x1300")
        master.mainloop()

    def setStartNumber(self,value):
        self.startListSelectedValue = value
    
    def setGoalNumber(self,value):
        self.goalListSelectedValue = value

    def beginNavigation(self):
        self.iBoilerObj.botBrain(str(self.startListSelectedValue),str(self.goalListSelectedValue),[(500,111)],0)
    
    def obtainResults(self):
        while(True):
            
            bigImg,img = self.iBoilerObj.botGod()
            if bigImg is None or img is None:
                pass
            else:
                bigImg = cv2.resize(bigImg,(650,900))
                img = cv2.resize(img,(900,900))
                bigPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(bigImg))
                photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
                self.canvasMapBig.create_image(0, 0, image=bigPhoto, anchor = NW)
                self.canvasMapZoom.create_image(0, 0, image=photo, anchor = NW)
            time.sleep(1)

    def startOperations(self,event):
        print('started')
        threadStart = threading.Thread(target=self.beginNavigation, daemon=True )
        threadResults = threading.Thread(target=self.obtainResults, daemon=True)
        threadStart.start()
        #t1 = time.time()
        #while(t)
        time.sleep(3)
        threadResults.start()

    


    def stopOperations(self,event):
        print("stopped")

class guiStart:
    def __init__(self):
        gui()

a = guiStart()

#if __name__ == "__main__":
    #gui = iBoilerGui()


#a = iBoiler('physics_corrected.jpg','Database/db',4,5,5,10,4.32,3.18,0.7,1)
#a.botBrain('R112','R121',[(500,111)],-90)