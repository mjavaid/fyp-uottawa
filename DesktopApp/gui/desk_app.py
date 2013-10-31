from tkinter import *
import sys

mGui = Tk()
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
mGui.mainloop()
