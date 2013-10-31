from tkinter import *
import sys
def mhello():
    #mlabel = Label(mGui, text = "Hello World").pack()
    #put an text box instead of a label
    mtext = hamed.get() #store the text in mtext
    mlabel2 = Label(mGui, text = mtext).pack()

def mNew():
    mlabel3 = Label(mGui, text = "You clicked ""New""").pack()
    

#in 2.7 it's TK() but in 3.3 the case sensitivity is changed
mGui = Tk()
hamed = StringVar()
#setting up the window to the size we want 
mGui.geometry("450x450+200+200")
#setting up a title
mGui.title("My GUI Example")

#creating a label and putting it on the screen using grid 
aLabel = Label(text = "My label", fg = "yellow", bg = "black").grid(row = 0, column = 0, sticky = W)
#aLabel2 = Label(text = "My second label", fg = "black", bg = "yellow").grid(row = 1, column = 0, sticky = W)
#aLabel3 = Label(text = "My third label", fg = "black", bg = "yellow").grid(row = 0, column = 1)
#aLabel4 = Label(text = "My fouth label", fg = "black", bg = "yellow").grid(row =1, column = 1)
#putting the label on the screen using pack
#the pack command puts everything in the center of the screen 
#aLabel.pack()
#aLabel2.pack()

#creating a button and functioning a button work
aButton = Button(mGui, text = "OK", command = mhello, fg = "red").grid(row = 1, column = 0, sticky = W)

#make an entry box
#watever is entered in the box -> will be stored in hamed
mEntry = Entry(mGui, textvariable = hamed).grid(row = 3, column = 0)


#menu construction
#1. make an menu bar
menubar = Menu(mGui)
#2. creating the items
fileMenu = Menu(menubar, tearoff = 0)
#3. adding list
fileMenu.add_command(label = "New", command = mNew)
fileMenu.add_command(label = "Open")
#fileMenu.add_command(Label = "Open")
#cascading them into list, call it file and take the file menu list and add it to the menu
menubar.add_cascade(label = "File", menu = fileMenu)
#appear it on the screen
mGui.config(menu = menubar)
















#on a windows machine you need to put this, on linux you don't need to do it
mGui.mainloop()

