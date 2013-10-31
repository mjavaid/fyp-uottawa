from tkinter import *
import sys

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
        canvas = Canvas(self.deskApp, height=35, width=450, bg="lightblue")
        canvas.pack()
        scanButton = Button(canvas, text="Scan")
        scanButton.place(x=10,y=7)
        uploadButton = Button(canvas, text="Upload")
        uploadButton.place(x=60,y=7)

    def runGUI(self):
        """Hangs the Python CLI if invoked"""
        self.deskApp.mainloop()

gui = GUI([None, None])
#gui.runGUI()
