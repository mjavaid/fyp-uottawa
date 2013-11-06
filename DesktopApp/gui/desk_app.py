import socket
from tkinter import *
beagleboneIP = '192.168.43.39'

import sys

#defining functions

def mAbout():
    messagebox.showinfo(title = "About", message = "about message")
    return

def mQuit():
    mExit = messagebox.askyesno(title = "Quit", message = "Are you certain you want to quit")
    if(mExit > 0): #making a boolean statement. 0 = false -> no
        mGui.destroy()
        return

def findingIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((beagleboneIP, 22))
        messagebox.showinfo(title = "Scanning...", message = "Found IP address")
    except TimeoutError:
        messagebox.showinfo(title = "Scanning...", message = "IP address Not Found")
    """if s.connect((beagleboneIP,22)):
        messagebox.showinfo(title = "Scanning...", message = "Found IP address")
    else:
        messagebox.showinfo(title = "Scanning...", message = "NOT found IP address")"""
    
        
    


mGui = Tk()
hamed = StringVar()
#setting up the window to the size we want 
mGui.geometry("450x450")
#setting up a title
mGui.title("DesktopApp")

#creating a canvas where the buttons will be on it
mCanvas1 = Canvas(mGui, height = 35, width = 450, bg = "darkblue")
mCanvas1.pack()

#creating another canvas where it would include a text box plus a button
mCanvas2 = Canvas(mGui, height = 30, width = 450, bg = "lightgray")
mCanvas2.pack()

#creating scan button 
mButton1 = Button(mCanvas1, text = "Scan", command = findingIp) #font = "bold"#
mButton1.place(x = 10, y = 5)

#creating upload button
mButton2 = Button(mCanvas1, text = "Upload") #font = "bold"
mButton2.place( x = 60, y = 5)

#Creating execute button
mButton3 = Button(mCanvas2, text = "Execute")
mButton3.place( x = 350, y = 5)

#Creating a text box
mEntry = Entry(mCanvas2, width = 50).place(x = 10, y = 8)

#creating a message dialogue box


#menu construction
#1. make an menu bar
menubar = Menu(mGui)
#creating file menu
fileMenu = Menu(menubar, tearoff = 0)
#creating a list
fileMenu.add_command(label = "Scan")
fileMenu.add_command(label = "Upload data")
fileMenu.add_command(label = "Close", command = mQuit)
#cascading them into list, call it file and take the file menu list and add it to the menu
menubar.add_cascade(label = "File", menu = fileMenu)


#creating edit menu
editMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Edit", menu = editMenu)

#creating help menu
helpMenu = Menu(menubar, tearoff = 0)
helpMenu.add_command(label = "About", command = mAbout)
menubar.add_cascade(label = "Help", menu = helpMenu)

#appear the menu on the screen
mGui.config(menu = menubar)


#on a windows machine you need to put this, on linux you don't need to do it
mGui.mainloop()
