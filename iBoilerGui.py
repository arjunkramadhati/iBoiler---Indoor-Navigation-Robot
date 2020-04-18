from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as font
        
class Window(Frame):
    def __init__(self, mapImage):
        master = Tk()
        Frame.__init__(self, master)
        self.mapImage = mapImage
        self.pack()

        print(self.mapImage)

        #GuiBuilder().root

        canvasWeidth = 300
        canvasHeight = 600

        # Map 
        w = Canvas(master, width=canvasWeidth, height=canvasHeight)
        w.place(x=30, y=30)
    
        load = Image.open(self.mapImage)
        width, height = load.size  
        print(width, height)
        newsize = (300, 600)
        load = load.resize(newsize)
        render = ImageTk.PhotoImage(load)
        w.create_image(0, 0, anchor=NW ,image=render)
        w.create_rectangle(55,55,65,65, fill='red')

        # Zoomed-in map
        w2 = Canvas(master, width=canvasWeidth, height=canvasHeight)
        w2.place(x=650, y=30)
    
        load2 = Image.open(self.mapImage)
        width, height = load.size  
        print(width, height)
        newsize = (300, 600)
        load2 = load2.resize(newsize)
        render2 = ImageTk.PhotoImage(load2)
        w2.create_image(0, 0, anchor=NW ,image=render2)
        w2.create_rectangle(55,55,65,65, fill='red')

        fontSize1 = font.Font(size=15)

        # Drop down for goal position
        label_goal = Label(master, text='Goal position')
        label_goal.place(x=350, y=30)
        label_goal['font'] = fontSize1

        OPTIONS = [
            "Room 111",
            "Room 112",
            "Room 113"
        ]

        variable = StringVar(master)
        variable.set(OPTIONS[0]) # default value

        option = OptionMenu(master, variable, *OPTIONS)
        option['font'] = fontSize1
        option.place(x=350, y=60)

        # Message box displaying the current coordinate and speed of the robot
        label_msg = Label(master, text='Message')
        label_msg.place(x=350, y=100)
        label_msg['font'] = fontSize1

        msg = Entry(master).place(x=350, y=130, width=250, height=250)

        # Buttons 
        fontSize = font.Font(size=20)

        btn_go = Button(master, text="GO!")
        #btn.grid(column=1, row=2)
        btn_go.place(x=425, y=400)
        btn_go['font'] = fontSize

        btn_stop = Button(master, text="STOP")
        #btn.grid(column=1, row=1)
        btn_stop.place(x=425, y=475)
        btn_stop['font'] = fontSize
                                
        btn_reset = Button(master, text="RESET")
        #btn.grid(column=1, row=1)
        btn_reset.place(x=425, y=550)
        btn_reset['font'] = fontSize

        master.wm_title("iBoiler Simulation")
        master.geometry("1000x650")
        master.mainloop()
    
    
if __name__ == '__main__':
    Window(mapImage="map.jpg")
    