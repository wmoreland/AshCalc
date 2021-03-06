import tkinter
from tkinter.ttk import Entry, Notebook, Frame, Scrollbar
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from desktop import helper_functions

class CutDownNavigationToolbar(NavigationToolbar2Tk):
	# only display the buttons needed
	toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] in ("Home", "Pan", "Save")]

	# Get ride of mode text
	def pan(self):
	    NavigationToolbar2Tk.pan(self)
	    self.mode = ""
	    self.set_message(self.mode)

	def zoom(self):
	    NavigationToolbar2Tk.zoom(self)
	    self.mode = ""
	    self.set_message(self.mode)

class CustomEntry(Entry):

	def __init__(self,*args,**kwargs):
		Entry.__init__(self,*args,**kwargs)
		self.userEditable = True

	def setUserEditable(self,userEditable):
		self.userEditable = userEditable
		self.config(state=(tkinter.ACTIVE if userEditable else tkinter.DISABLED))

	def insertNew(self,text):
		if not self.userEditable:
			self.config(state="normal")
		self.delete(0,tkinter.END)
		self.insert(0,text)
		if not self.userEditable:
			self.config(state="readonly")

class NumericEntry(CustomEntry):

	trueValue = None
	sf = None

	def setSF(self, sf):
		self.sf = sf

	def insertNew(self,value):
		self.trueValue = value
		value = helper_functions.roundToSF(value, self.sf)
		super(NumericEntry, self).insertNew(value)

	def get(self):
		value = super(CustomEntry, self).get()
		if helper_functions.roundToSF(self.trueValue, self.sf) == value:
			return self.trueValue
		else:
			return value

class ImprovedNotebook(Notebook):

	def __init__(self,*args,**kwargs):
		Notebook.__init__(self,*args,**kwargs)
		self.currentFrames = set()

	def addFrame(self,frame,text):
		if frame not in self.currentFrames:
			self.add(frame,text=text)
			self.currentFrames.add(frame)

	def removeFrame(self,frame):
		if frame in self.currentFrames:
			self.forget(frame)
			self.currentFrames.remove(frame)

class ScrollFrame(Frame):

	def __init__(self,parent):

		Frame.__init__(self, master=parent)

		canvas = tkinter.Canvas(self, highlightthickness=0)
		self.innerFrame = Frame(canvas)

		myscrollbar = Scrollbar(self, orient="vertical")
		myscrollbar.configure(command=canvas.yview)

		def scrollbarSet(top, bottom):
			# Hides and shows the scroll frame depending on need
			if float(top) > 0 or float(bottom) < 1:
				myscrollbar.grid(row=0, column=1, sticky="NS")
			else:
				pass
				myscrollbar.grid_remove()
			myscrollbar.set(top, bottom)
		canvas.configure(yscrollcommand = scrollbarSet)


		configureFunc = lambda _ :  canvas.configure(scrollregion=canvas.bbox("all"))
		frameID = canvas.create_window((0,0), window=self.innerFrame, anchor='nw')
		self.innerFrame.bind("<Configure>",configureFunc)

		canvas.grid(row=0, column=0, sticky="NSEW")
		myscrollbar.grid(row=0, column=1, sticky="NS")
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=0)


		#canvas.bind("<Configure>", lambda e : canvas.itemconfig(frameID, width=e.width))
		canvas.bind("<Configure>", lambda e : canvas.configure(width=self.innerFrame.winfo_width()))
