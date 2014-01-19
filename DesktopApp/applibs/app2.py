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

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class APPLICATION(Tk):
    COMMAND = None
    
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
        connectBtn = ttk.Button(actionFrame, text="Connect", command=self.connectHandler)
        
        uploadBtn.grid(column=0, row=0, sticky=(W))
        connectBtn.grid(column=1, row=0, sticky=(W))
        
        actionFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        """ End_Action_Button """
        
        ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E,W))
        
        """ Command_Execute_UI """
        executeFrame = ttk.Frame(window, padding=(5,5))
        
        cmdEntry = ttk.Entry(executeFrame, textvariable=self.COMMAND, width=50)
        executeBtn = ttk.Button(executeFrame, text="Execute", command=self.executeHandler)
        
        cmdEntry.grid(column=0, row=0, sticky=(W))
        executeBtn.grid(column=1, row=0, sticky=(W))
        
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
            self.plotHandler({'x': plot[0], 'y': plot[1]})
        fh.close()
    
    def connectHandler(self):
        print("TODO: Connect")
    
    def executeHandler(self):
        print("TODO: Execute")
    
    def aboutHandler(self):
        print("TODO: About")
    
    def manualHandler(self):
        print("TODO: Manual")
    
    def quitHandler(self):
        shouldQuit = messagebox.askquestion("Quit", "Exit the application?", icon="warning")
        if shouldQuit == "yes": self.quit()

    def plotHandler(self, data=None):
        if data == None: return
        self.ax.scatter(data['x'], data['y'])
        self.canvas.draw()

if __name__ == '__main__':
    app = APPLICATION()
    app.mainloop()
