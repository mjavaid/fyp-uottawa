# File: app.py
# Project: 3D-EMR
# Created: 1/10/14
# Auther: Muhammad Javaid

try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
except ImportError:
    from Tkinter import *
    import ttk
    import tkFileDialog as filedialog

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
        
        cmdEntry = ttk.Entry(executeFrame, textvariable=self.COMMAND)
        executeBtn = ttk.Button(executeFrame, text="Execute", command=self.executeHandler)
        
        cmdEntry.grid(column=0, row=0, sticky=(W))
        executeBtn.grid(column=1, row=0, sticky=(W))
        
        executeFrame.grid(column=0, row=2, sticky=(N,S,E,W))
        """ End_Command_Execute_UI """
        
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
        plotData = fh.read()
        self.processPlotData(plotData)
        fh.close()
        print("TODO: Upload")
    
    def connectHandler(self):
        print("TODO: Connect")
    
    def executeHandler(self):
        print("TODO: Execute")
    
    def aboutHandler(self):
        print("TODO: About")
    
    def manualHandler(self):
        print("TODO: Manual")
    
    def quitHandler(self):
        print("TODO: Quit")
        self.quit()
    
    def processPlotData(self, plotData=None):
        if plotData == None:
            print("No Data Provided")
            return
        print("TODO: Process Plot Data")

    def plotData(self, plotData=None):
        if plotData == None:
            print("No Data Provided")
            return
        print("TODO: Plot Data")

if __name__ == '__main__':
    app = APPLICATION()
    app.mainloop()
