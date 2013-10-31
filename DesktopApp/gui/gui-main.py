from tkinter import *
import sys

"""mGui = Tk()
hamed = StringVar()
#setting up the window to the size we want 
mGui.geometry("450x450")
#setting up a title
mGui.title("DesktopApp")

#creating a canvas where the buttons will be on it
mCanvas = Canvas(mGui, height = 35, width = 450, bg = "lightblue")
mCanvas.pack()

#creating scan button 
mButton1 = Button(mCanvas, text = "Scan") #font = "bold"#
mButton1.place(x = 10, y = 5)

#creating upload button
mButton2 = Button(mCanvas, text = "Upload") #font = "bold"
mButton2.place( x = 60, y = 5)


#menu construction
#1. make an menu bar
menubar = Menu(mGui)
#2. creating the items
fileMenu = Menu(menubar, tearoff = 0)
#cascading them into list, call it file and take the file menu list and add it to the menu
menubar.add_cascade(label = "File", menu = fileMenu)
menubar.add_cascade(label = "Edit", menu = fileMenu)
menubar.add_cascade(label = "About", menu = fileMenu)

#appear it on the screen
mGui.config(menu = menubar)

#on a windows machine you need to put this, on linux you don't need to do it
mGui.mainloop()"""


DEFAULT_TITLE = "DesktopApp"            
DIMENSIONS, TITLE = 0, 1
DEFAULT_DIMENSIONS = "450x450"

class GUI:
    deskApp = None

    def __init__(self, ARGS):
        self.deskApp = Tk()
        self.constructGUI(ARGS)

    def constructGUI(self, ARGS):
        # Set Title
        if ARGS[TITLE]==None: self.deskApp.title(DEFAULT_TITLE)
        else: self.deskApp.title(ARGS[self.TITLE])
        # Set Dimensions
        if ARGS[DIMENSIONS]==None: self.deskApp.geometry(DEFAULT_DIMENSIONS)
        else: self.deskApp.geometry(ARGS[DIMENSIONS])
        # Create Menu
        menu = Menu(self.deskApp)
        fileMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Edit", menu=fileMenu)
        menu.add_cascade(label="About", menu=fileMenu)
        self.deskApp.config(menu=menu)
        # Create UI Buttons
        canvas1 = Canvas(self.deskApp, height=35, width=450, bg="lightblue")
        canvas1.place(x = 0, y = 0)
        canvas2 = Canvas(self.deskApp, height = 30, width = 450, bg ="lightgray")
        canvas2.place(x = 0, y = 35)
        scanButton = Button(canvas1, text="Scan")
        scanButton.place(x= 10,y=7)
        uploadButton = Button(canvas1, text="Upload")
        uploadButton.place(x=60,y=7)

    def runGUI(self):
        """Hangs the Python CLI if invoked"""
        self.deskApp.mainloop()

gui = GUI([None, None])
#gui.runGUI()
