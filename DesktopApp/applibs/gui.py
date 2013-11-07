from tkinter import *
from tkinter import messagebox
import sys
import connection

DEFAULT_TITLE = "DesktopApp"
DIMENSIONS, TITLE = 0, 1
DEFAULT_DIMENSIONS = "450x450"

class GUI(Frame):
	conn = None

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack()
		self.constructGUI()
		self.conn = connection.CONN()

	def constructGUI(self):
		# Create Menu
		self.menu = Menu(self.parent)
		self.parent.config(menu=self.menu)
		fileMenu = Menu(self.menu, tearoff=0)
		fileMenu.add_command(label="Upload", command=self.uploadHandler)
		fileMenu.add_command(label="Exit", command=lambda: self.quitHandler(self.parent))
		self.menu.add_cascade(label="File", menu=fileMenu)
		editMenu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Edit", menu=editMenu)
		helpMenu = Menu(self.menu, tearoff=0)
		helpMenu.add_command(label="About", command=self.aboutHandler)
		self.menu.add_cascade(label="Help", menu=helpMenu)
		# Create UI Buttons
		canvas1 = Canvas(self, height=35, width=450, bg="lightblue")
		canvas1.pack()#canvas1.place(x=0,y=0)
		canvas2 = Canvas(self, height=35, width=450, bg ="lightgray")
		canvas2.pack()#canvas2.place(x=0,y=35)
		scanButton = Button(canvas1, text="Connect", command=self.connDataDialogBox)
		scanButton.place(x=10,y=5)
		uploadButton = Button(canvas1, text="Upload", command=self.uploadHandler)
		uploadButton.place(x=75,y=5)
		executeButton = Button(canvas2, text="Execute", command=self.executeHandler)
		executeButton.place(x=260,y=6)
		self.entry = Entry(canvas2, width=40)
		self.entry.place(x=10,y=8)
		self.command = StringVar()
		self.command.set("")
		self.entry["textvariable"] = self.command

	def runGUI(self):
		"""Hangs the Python CLI if invoked"""
		self.mainloop()
	
	def connDataDialogBox(self):
		if self.conn.isConnected(): return
		top = self.top = Toplevel(self)
		
		hostLbl= Label(top, text="Host:")
		hostLbl.pack()
		self.host = Entry(top)
		self.host.pack()
		
		portLbl= Label(top, text="Port:")
		portLbl.pack()
		self.port = Entry(top)
		self.port.pack()

		submitBtn = Button(top, text='Submit', command=lambda: self.submitConnData(False))
		submitBtn.pack()

		defaultBtn = Button(top, text='Default', command=lambda: self.submitConnData(True))
		defaultBtn.pack()
		cancelBtn = Button(top, text='Cancel', command=lambda: self.top.destroy())
		cancelBtn.pack()

	def submitConnData(self, isDefault):
		ARGS = [None, None]
		if not isDefault:
			host = self.host.get()
			port = int(self.port.get())
			ARGS = []
			ARGS.append(host)
			ARGS.append(port)
		print(ARGS)
		self.top.destroy()
		self.connectHandler(ARGS)

	def aboutHandler(self):
		messagebox.showinfo(title="About", message="About Message")
		return

	def connectHandler(self, ARGS):
		resp = self.conn.connectToRobot(ARGS)
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
		cmd = self.command.get()
		resp = self.conn.sendMessage(cmd)
		print(resp)
		return
		
	def quitHandler(self, root):
		quit = messagebox.askyesno(title="Quit", message="Exit Program?")
		if quit: root.destroy()
		return

def createApp(ARGS):
	root = Tk()
	app = GUI(root)
	# Root Settings
	root.resizable(width=False, height=False)
	root.protocol("WM_DELETE_WINDOW", lambda: app.quitHandler(root))
	# Set Title
	if ARGS[TITLE]==None: app.master.title(DEFAULT_TITLE)
	else: app.master.title(ARGS[self.TITLE])
	# Set Dimensions
	if ARGS[DIMENSIONS]==None: app.master.geometry(DEFAULT_DIMENSIONS)
	else: app.master.geometry(ARGS[DIMENSIONS])
	return app

if __name__ == "__main__":
    app = createApp([None, None])
    app.runGUI()
