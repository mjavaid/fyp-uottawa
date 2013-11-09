from tkinter import *
from tkinter import messagebox
import sys

DEFAULT_TITLE = "DesktopApp"
DIMENSIONS, TITLE = 0, 1
DEFAULT_DIMENSIONS = "450x450"

class GUI():
    deskApp = None

    def __init__(self, ARGS):
        self.deskApp = Tk()
        self.deskApp.resizable(width=False, height=False)
        self.deskApp.protocol("WM_DELETE_WINDOW", self.quitHandler)
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
        fileMenu.add_command(label="Connect",command=self.connectHandler)
        fileMenu.add_command(label="Upload", command=self.uploadHandler)
        fileMenu.add_command(label="Terminate", command=self.terminateHandler)
        fileMenu.add_command(label="Exit", command=self.quitHandler)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editMenu)
        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="About", command=self.aboutHandler)
        menu.add_cascade(label="Help", menu=helpMenu)
        self.deskApp.config(menu=menu)
        # Create UI Buttons
        canvas1 = Canvas(self.deskApp, height=65, width=450, bg="darkblue")
        canvas1.pack()
        canvas2 = Canvas(self.deskApp, height=32, width=450, bg ="lightgray")
        canvas2.pack()
        connectbutton = Button(canvas1, text="Connect", width = 6, fg = "darkgreen", command=self.connectHandler)
        connectbutton.place(x=10,y=5)
        terminatebutton = Button(canvas1, text="Terminate", fg = "darkred", command=self.terminateHandler)
        terminatebutton.place(x=70,y=5)
        uploadButton = Button(canvas1, text="Upload",width = 6, command=self.uploadHandler)
        uploadButton.place(x=10,y=33)
        executeButton = Button(canvas2, text="Execute", bg = "green", command=self.executeHandler)
        executeButton.place(x=350,y=5)
        entry = Entry(canvas2, width=50).place(x=10,y=8)

    def runGUI(self):
        """Hangs the Python CLI if invoked"""
        self.deskApp.mainloop()

    def aboutHandler(self):
        messagebox.showinfo(title="About", message="About Message")
        return

    def quitHandler(self):
        choice = messagebox.askyesno(title="Quit", message="Exit Program?")
        if choice != 0: self.deskApp.destroy()
        return

    def connectHandler(self):
        messagebox.showinfo(title="Scanning", message="404: Robot Not Found")
        return


    def terminateHandler(self):
        messagebox.showinfo(title="Terminating", message="404: Not connection to terminate")
        return

    def uploadHandler(self):
        messagebox.showinfo(title="Upload", message="Upload File")
        return

    def executeHandler(self):
        messagebox.showinfo(title="Execute", message="Executing Command")
        return

gui = GUI([None, None])
gui.runGUI()
