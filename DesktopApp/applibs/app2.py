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

lastx, lasty = 0, 0

plot2DCanvas = None

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):
    global lastx, lasty, plot2DCanvas
    plot2DCanvas.create_line((lastx, lasty, event.x, event.y))
    lastx, lasty = event.x, event.y

def uploadHandler(event=None):
    print("Upload Handler")
    filename = filedialog.askopenfilename(filetypes=(('3D EMR', '*.emr'),('All Files', '*.*')))
    print(filename)

def executeHandler(event=None):
    print("Execute Handler")
    #plotMap()

def connectHandler(event=None):
    print("Connect Handler")
    #print(plot2DCanvas.winfo_width())
    #plot2DCanvas.config(width=(plot2DCanvas.winfo_width()+10))

def aboutHandler(event=None):
    aboutWindow = Toplevel()
    aboutWindow.title('About')
    aboutWindow.resizable(FALSE, FALSE)

class COORDINATES:
    x = None
    y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y

def plotMap(event=None):
    for i in range(20):
        coord = COORDINATES(i*10, i*100)
        addLine(coord)

def createGUI(app=None):
    if app == None:
        print("No App Provided")
        return
    
    global plot2DCanvas

    menubar = Menu(app)
    menu_file = Menu(menubar)
    menu_file.add_command(label='Upload', command=uploadHandler)
    menu_file.add_command(label='Connect', command=connectHandler)
    menu_file.add_separator()
    menu_file.add_command(label='Quit', command=app.quit)

    menu_help = Menu(menubar)
    menu_help.add_command(label='About', command=aboutHandler)

    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_cascade(menu=menu_help, label='Help')

    app.configure(menu=menubar)

    window = ttk.Frame(app)
    actionButtonsFrame = ttk.Frame(window, padding=(5, 5))
    executeOptionsFrame = ttk.Frame(window, padding=(5, 5))

    canvasFrame = ttk.Frame(window)
    h = ttk.Scrollbar(canvasFrame, orient=HORIZONTAL)
    v = ttk.Scrollbar(canvasFrame, orient=VERTICAL)
    plot2DCanvas = Canvas(canvasFrame, scrollregion=(0, 0, 700, 700), width=500, height=500, yscrollcommand=v.set, xscrollcommand=h.set, bg='#eee')
    h['command'] = plot2DCanvas.xview
    v['command'] = plot2DCanvas.yview
    ttk.Sizegrip(canvasFrame).grid(column=1, row=1, sticky=(N,W,S,E))
    plot2DCanvas.grid(column=0, row=0, sticky=(N,S,E,W))
    h.grid(column=0,row=1,sticky=(W,E))
    v.grid(column=1,row=0,sticky=(N,S))
    canvasFrame.grid_columnconfigure(0,weight=1)
    canvasFrame.grid_rowconfigure(0, weight=1)

    plot2DCanvas.bind("<Button-1>", lambda event: xy(event))
    plot2DCanvas.bind("<B1-Motion>", lambda event: addLine(event))

    """canvasFrame = ttk.Frame(window, width=500, height=500)
    canvasFrame.rowconfigure(0, weight=1)
    canvasFrame.columnconfigure(0, weight=1)

    plot2DCanvas = Canvas(canvasFrame)
    plot2DCanvas.grid(column=0, row=0, sticky=(N, S, E, W))
    scrollb = Scrollbar(canvasFrame, command=plot2DCanvas.yview)
    scrollb.grid(row=0, column=1, sticky=(N, S, E, W))
    plot2DCanvas.config(yscrollcommand=scrollb.set)"""


    """plot2DCanvas = Canvas(canvasFrame, width=500, height=500)
    hbar = Scrollbar(canvasFrame, orient=HORIZONTAL, command=plot2DCanvas.xview)
    hbar.grid(column=0, row=1, sticky=(E, W, S))
    vbar = Scrollbar(canvasFrame, orient=VERTICAL, command=plot2DCanvas.yview)
    vbar.grid(column=1, row=0, sticky=(N, S, E))
    plot2DCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    plot2DCanvas.grid_columnconfigure(0, weight=1)
    canvasFrame.grid_columnconfigure(0, weight=1)"""

    #uploadImg = PhotoImage(file='../resources/images/upload.gif')
    uploadBtn = ttk.Button(actionButtonsFrame, text='Upload', command=uploadHandler)
    connectBtn = ttk.Button(actionButtonsFrame, text='Connect', command=connectHandler)

    executeBtn = ttk.Button(executeOptionsFrame, text='Execute', command=executeHandler)
    cmd = StringVar()
    commandEntry = ttk.Entry(executeOptionsFrame, textvariable=cmd, width=50)

    window.grid(column=0, row=0, sticky=(N, S, E, W))
    actionButtonsFrame.grid(column=0, row=0, sticky=(E, W))
    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E, W))
    executeOptionsFrame.grid(column=0, row=2, sticky=(E, W))
    ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=3, sticky=(E, W))
    canvasFrame.grid(column=0, row=4, sticky=(N, S, E, W))

    uploadBtn.grid(column=0, row=0, sticky=(W))
    connectBtn.grid(column=1, row=0, sticky=(W))

    commandEntry.grid(column=0, row=0, sticky=(W))
    executeBtn.grid(column=1, row=0, sticky=(W))

if __name__ == '__main__':
    app = Tk()
    app.title('3D-EMR Desktop Application')
    app.option_add('*tearOff', FALSE)
    app.resizable(FALSE, FALSE)

    app.bind('<Command-u>', uploadHandler)
    app.bind('<Control-u>', uploadHandler)
    app.bind('<Command-e>', executeHandler)
    app.bind('<Control-e>', executeHandler)
    app.bind('<Command-r>', connectHandler)
    app.bind('<Control-r>', connectHandler)

    createGUI(app)

    app.mainloop()
