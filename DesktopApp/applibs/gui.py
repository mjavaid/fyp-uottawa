from tkinter import *
from tkinter import messagebox
import sys
import connection

DEFAULT_TITLE = "DesktopApp"            
DIMENSIONS, TITLE = 0, 1
DEFAULT_DIMENSIONS = "450x450"

class GUI:
    deskApp = None
    conn = None

    def __init__(self, ARGS):
        self.deskApp = Tk()
        self.deskApp.resizable(width=False, height=False)
        self.deskApp.protocol("WM_DELETE_WINDOW", self.quitHandler)
        self.constructGUI(ARGS)
        self.conn = connection.CONN()

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
        fileMenu.add_command(label="Upload", command=self.uploadHandler)
        fileMenu.add_command(label="Exit", command=self.quitHandler)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editMenu)
        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="About", command=self.aboutHandler)
        menu.add_cascade(label="Help", menu=helpMenu)
        self.deskApp.config(menu=menu)
        # Create UI Buttons
        canvas1 = Canvas(self.deskApp, height=35, width=450, bg="lightblue")
        canvas1.place(x=0,y=0)
        canvas2 = Canvas(self.deskApp, height=35, width=450, bg ="lightgray")
        canvas2.place(x=0,y=35)
        scanButton = Button(canvas1, text="Connect", command=self.connectHandler)
        scanButton.place(x=10,y=5)
        uploadButton = Button(canvas1, text="Upload", command=self.uploadHandler)
        uploadButton.place(x=75,y=5)
        executeButton = Button(canvas2, text="Execute", command=self.executeHandler)
        executeButton.place(x=260,y=6)
        entry = Entry(canvas2, width=40).place(x=10,y=8)

    def runGUI(self):
        """Hangs the Python CLI if invoked"""
        self.deskApp.mainloop()

    def aboutHandler(self):
        messagebox.showinfo(title="About", message="About Message")
        return

    def quitHandler(self):
        quit = messagebox.askyesno(title="Quit", message="Exit Program?")
        if quit: self.deskApp.destroy()
        return

    def connectHandler(self):
        resp = self.conn.connectToRobot()
        if resp == self.conn.CONN_TIMEOUT_ERR:
            messagebox.showinfo(title="Timeout Error", message="Connection Timed Out")
        elif resp == self.conn.CONN_REFUSED_ERR:
            messagebox.showinfo(title="Connection Refused Error", message="Connection To Robot Refused")
        elif resp == self.conn.NO_ERR:
            messagebox.showinfo(title="Connected", message="Connection Established")
        return

    def uploadHandler(self):
        messagebox.showinfo(title="Upload", message="Upload File")
        return

    def executeHandler(self):
        messagebox.showinfo(title="Execute", message="Executing Command")
        return

if __name__ == "__main__":
    gui = GUI([None, None])
    gui.runGUI()
