import tkinter as tk

class App:
	def __init__(self):
		self._root = tk.Tk()
		
		self._root.title("Stagger")
		self._root.protocol("WM_DELETE_WINDOW", self.applicationExit)
		self._root.minsize(700,700)
		
	def mainLoop(self):
		"""
		Accessor for member function of protecteted member root
		:return: None
		"""
		
		self._root.mainloop()
		
	def applicationExit(self):
		"""
		If anything else needs to be done between clicking X and the program closing, add it here
		
		Or, call this if the program ever needs to be closed from elsehwre in the program.
		:return: None
		"""
		self._root.destroy()