# File: app.py
# Project: 3D-EMR
# Created: 1/10/14
# Auther: Muhammad Javaid

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

lastx, lasty = 0, 0

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):
    global lastx, lasty
    plot2DCanvas.create_line((lastx, lasty, event.x, event.y))
    lastx, lasty = event.x, event.y

def uploadHandler(event=None):
    print("Upload Handler")
    filename = filedialog.askopenfilename()
    print(filename)

def executeHandler(event=None):
    print("Execute Handler")

def connectHandler(event=None):
    print("Connect Handler")
    plot2DCanvas.config(width=700)

def aboutHandler(event=None):
    aboutWindow = Toplevel()
    aboutWindow.title('About')
    aboutWindow.resizable(FALSE, FALSE)

app = Tk()
app.title('3D-EMR Desktop Application')
app.option_add('*tearOff', FALSE)
app.resizable(FALSE, FALSE)

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
plot2DCanvas = Canvas(canvasFrame, width=1000, height=1000)
hbar = Scrollbar(canvasFrame, orient=HORIZONTAL, command=plot2DCanvas.xview)
hbar.grid(column=0, row=1, sticky=(E, W))
vbar = Scrollbar(canvasFrame, orient=VERTICAL, command=plot2DCanvas.yview)
vbar.grid(column=1, row=0, sticky=(N, S))
plot2DCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
plot2DCanvas.grid_columnconfigure(0, weight=1)

#uploadImg = PhotoImage(file='../resources/images/upload.gif')
uploadBtn = ttk.Button(actionButtonsFrame, text='Upload', command=uploadHandler)
connectBtn = ttk.Button(actionButtonsFrame, text='Connect', command=connectHandler)

executeBtn = ttk.Button(executeOptionsFrame, text='Execute', command=executeHandler)
cmd = StringVar()
commandEntry = ttk.Entry(executeOptionsFrame, textvariable=cmd)

window.grid(column=0, row=0, sticky=(N, S, E, W))
actionButtonsFrame.grid(column=0, row=0, sticky=(E, W))
ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E, W))
executeOptionsFrame.grid(column=0, row=2, sticky=(E, W))
ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=3, sticky=(E, W))
canvasFrame.grid(column=0, row=4, sticky=(N, S, E, W))

plot2DCanvas.grid(column=0, row=0, sticky=(N, S, E, W))
plot2DCanvas.bind("<Button-1>", xy)
plot2DCanvas.bind("<B1-Motion>", addLine)

uploadBtn.grid(column=0, row=0, sticky=(W))
connectBtn.grid(column=1, row=0, sticky=(W))

commandEntry.grid(column=0, row=0, sticky=(W))
executeBtn.grid(column=1, row=0, sticky=(W))

app.bind('<Command-u>', uploadHandler)
app.bind('<Command-e>', executeHandler)
app.bind('<Command-r>', connectHandler)

app.mainloop()
