# File: app.py
# Project: 3D-EMR
# Created: 1/10/14
# Auther: Muhammad Javaid

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

import csv

import time

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import threading
import connection as conn

from math import sin, cos, radians

App = None
Connection = None
closeConnection = False

class Application(Tk):
    COMMAND = None
    X_OFFSET = 0
    Y_OFFSET = 0
    FACING_ANGLE = 90
    LENGTH_PER_MOVEMENT = 34
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("3D-EMR App")
        self.resizable(False, False)
        self.wm_protocol("WM_DELETE_WINDOW", self.quitHandler)
        self.option_add("*tearOff", FALSE)
        self.COMMAND = StringVar()
        self.createGUI()
        self.bind('<Command-u>', self.uploadHandler)
        self.bind('<Control-u>', self.uploadHandler)
        self.bind('<Command-e>', self.executeHandler)
        self.bind('<Control-e>', self.executeHandler)
        self.bind('<Command-r>', self.connectHandler)
        self.bind('<Control-r>', self.connectHandler)
    
    def createGUI(self):
        """ Menubar """
        menubar = Menu(self)
        
        filemenu = Menu(menubar)
        filemenu.add_command(label="Upload", command=self.uploadHandler)
        filemenu.add_command(label="Save", command=self.saveHandler)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quitHandler)
        
        actionmenu = Menu(menubar)
        actionmenu.add_command(label="Connect", command=self.connectHandler)
        actionmenu.add_command(label="Execute", command=self.executeHandler)
        actionmenu.add_command(label="Plot", command=self.plotHandler)
        
        helpmenu = Menu(menubar)
        helpmenu.add_command(label="About", command=self.aboutHandler)
        helpmenu.add_command(label="Manual", command=self.manualHandler)
        
        menubar.add_cascade(menu=filemenu, label="File")
        menubar.add_cascade(menu=actionmenu, label="Actions")
        menubar.add_cascade(menu=helpmenu, label="Help")
        
        self.configure(menu=menubar)
        """ End_Menubar """
        
        window = ttk.Frame(self)
        
        """ Action_Buttons """
        actionFrame = ttk.Frame(window, padding=(5,5))
        
        uploadBtn = ttk.Button(actionFrame, text="Upload", command=self.uploadHandler)
        saveBtn = ttk.Button(actionFrame, text="Save", command=self.saveHandler)
        ttk.Separator(actionFrame, orient=VERTICAL).grid(column=2, row=0, sticky=(N,S), padx=5)
        connectBtn = ttk.Button(actionFrame, text="Connect", command=self.connectHandler)
        disconnectBtn = ttk.Button(actionFrame, text="Disconnect", command=self.disconnectHandler)
        
        uploadBtn.grid(column=0, row=0, sticky=(W))
        saveBtn.grid(column=1, row=0, sticky=(W))
        connectBtn.grid(column=3, row=0, sticky=(W))
        disconnectBtn.grid(column=4, row=0, sticky=(W))
        
        actionFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        """ End_Action_Button """
        
        ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E,W))
        
        """ Command_Execute_UI """
        executeFrame = ttk.Frame(window, padding=(5,5))
        
        cmdEntry = ttk.Entry(executeFrame, textvariable=self.COMMAND, width=50)
        executeBtn = ttk.Button(executeFrame, text="Execute", command=self.executeHandler)
        
        cmdEntry.grid(column=0, row=0, sticky=(W))
        executeBtn.grid(column=1, row=0, sticky=(W), padx=5)
        
        executeFrame.grid(column=0, row=2, sticky=(N,S,E,W))
        """ End_Command_Execute_UI """
        
        ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=3, sticky=(E,W))
        
        """ Plotting_Canvas """
        canvasFrame = ttk.Frame(window)
        
        figure = Figure()
        self.ax = figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(figure, master=canvasFrame)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=(N,S,E,W))
        self.canvas.show()
        
        toolbar = NavigationToolbar2TkAgg(self.canvas, canvasFrame)
        toolbar.grid(column=0, row=1, sticky=(E,W))
        toolbar.update()
        
        canvasFrame.grid(column=0, row=4)
        """ End_Plotting_Canvas """
        
        window.grid(column=0, row=0, sticky=(N,S,E,W))
    
    def uploadHandler(self):
        filename = filedialog.askopenfilename(filetypes=(
            ("3D-EMR Files", "*.emr"),
            ("XY Files", "*.xy"),
            ("CSV Files", "*.csv"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ))
        if filename == "": return
        fh = open(filename, "r")
        fileContents = (fh.read()).split("\n")
        plotData = [result.split(",") for result in fileContents if result != ""]
        for plot in plotData:
            self.plotHandler(plot)
        fh.close()
    
    def connectHandler(self):
        connectWindow = Toplevel()
        connectWindow.title("Connect To Robot")
        connectWindow.resizable(False, False)
        
        HOST = StringVar()
        PORT = StringVar()
        
        actionFrame = ttk.Frame(connectWindow, padding=(10, 10))
        
        hostLabel = ttk.Label(actionFrame, text="Host:")
        portLabel = ttk.Label(actionFrame, text="Port:")
        
        hostEntry = ttk.Entry(actionFrame, textvariable=HOST)
        portEntry = ttk.Entry(actionFrame, textvariable=PORT)
        
        connectBtn = ttk.Button(actionFrame, text="Connect", command=lambda: self.testConnect(connectWindow, HOST, PORT))
        useDefaultBtn = ttk.Button(actionFrame, text="Use Default", command=lambda: self.testConnect(connectWindow))
        cancleBtn = ttk.Button(actionFrame, text="Cancel", command=connectWindow.destroy)
        
        hostLabel.grid(column=0, row=0, sticky=(E), padx=5)
        hostEntry.grid(column=1, row=0, sticky=(E,W))
        portLabel.grid(column=0, row=1, sticky=(E), padx=5)
        portEntry.grid(column=1, row=1, sticky=(E,W))
        ttk.Separator(actionFrame, orient=HORIZONTAL).grid(row=2, columnspan=3, sticky=(E,W), pady=10)
        connectBtn.grid(column=0, row=3)
        useDefaultBtn.grid(column=1, row=3)
        cancleBtn.grid(column=2, row=3)
        
        actionFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        
        print("TODO: Connect")
    
    def testConnect(self, connectWindow, host=None, port=None):
        createConnection(host, port)
        connectWindow.destroy()
    
    def disconnectHandler(self):
        global closeConnection
        print(conn.sendMessage("CLOSE_CONNECTION"))
        closeConnection = True
    
    def executeHandler(self):
        print("TODO: Execute")
        cmd = self.COMMAND.get()
        self.COMMAND.set("")
        cmd = cmd.upper()
        _, response = conn.sendMessage(cmd)
        if cmd.upper() == "SCAN":
            done = False
            overflow = False
            dOverflow = 0
            while not done:
                vectors = response.split(";")
                for vector in vectors:
                    args = vector.split(",")
                    if len(args) == 2:
                        if overflow:
                            h, angle = dOverflow, args[0]
                            overflow = False
                            dOverflow = 0
                        else:
                            h, angle = args[0], args[1]
                        h, angle = float(h), float(angle)
                        if h > 0:
                            A = ((90 + self.FACING_ANGLE) % 360 ) - angle
                            if A < 0: 
                                A = 360 + A
                            x, y = (cos(radians(A)) * h) + self.X_OFFSET, (sin(radians(A)) * h) + self.Y_OFFSET
                            print x,y,h,angle
                            App.plotHandler([x, y])
                    else:
                        overflow = True
                        dOverflow = args[0]
                if angle == 180.0:
                    done = True
                else:
                    _, response = conn.sendMessage("")
        elif "MOVE" in cmd:
            print "MOVE"
            args = cmd.split(" ")
            print args
            n = int(args[2])
            direction = args[1]
            if direction == "RIGHT":
                n = n % 360
                n = 360 - n
                self.FACING_ANGLE = (self.FACING_ANGLE + n) % 360
            elif direction == "LEFT":
                n = n % 360
                self.FACING_ANGLE = (self.FACING_ANGLE + n) % 360
            elif direction == "FORWARD":
                self.X_OFFSET = (cos(radians(self.FACING_ANGLE)) * n * self.LENGTH_PER_MOVEMENT) + self.X_OFFSET
                self.Y_OFFSET = (sin(radians(self.FACING_ANGLE)) * n * self.LENGTH_PER_MOVEMENT) + self.Y_OFFSET
            elif direction == "BACKWARDS":
                A = ((180 + self.FACING_ANGLE) % 360)
                self.X_OFFSET = (cos(radians(A)) * n * self.LENGTH_PER_MOVEMENT) + self.X_OFFSET
                self.Y_OFFSET = (sin(radians(A)) * n * self.LENGTH_PER_MOVEMENT) + self.Y_OFFSET
        
    def aboutHandler(self):
        print("TODO: About")
    
    def manualHandler(self):
        print("TODO: Manual")
    
    def quitHandler(self):
        shouldQuit = messagebox.askquestion("Quit", "Exit the application?", icon="warning")
        if shouldQuit == "yes": self.quit()

    def plotHandler(self, data=None):
        if data == None: return
        self.ax.scatter(data[0], data[1])
        self.canvas.draw()

    def saveHandler(self):
        print("TODO: Save")

    def executeGUI(self):
        self.mainloop()

class connectionThread(threading.Thread):
    def __init__(self, threadID, name, host=None, port=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.host = host
        self.port = port
        
    def run(self):
        global closeConnection, App
        if self.host == None or self.port == None: dest = None
        else: dest = [self.host, self.port]
        conn.connect(dest)
        """SEND_DATA_CMD = "GET_DATA_STREAM"
        _, data = conn.sendMessage(SEND_DATA_CMD)
        if data == "ACK_GDS":
            while not closeConnection:
                SEND_ACK = "ACK"
                _, data = conn.sendMessage(SEND_ACK)
                plotData = data.split(",")
                plotData[0], plotData[1] = int(plotData[0]), int(plotData[1])
                App.plotHandler(plotData)"""
        while not closeConnection:
            continue
        print "DISCONNECTING..."
        conn.closeConnection()

def createApplication():
    global App
    App = Application()
    return App

def createConnection(host=None, port=None):
    if not host == None and not port == None: host, port = host.get(), int(port.get())
    connection = connectionThread(1, "connection", host, port)
    connection.start()

if __name__ == '__main__':
    createApplication()
    App.executeGUI()
