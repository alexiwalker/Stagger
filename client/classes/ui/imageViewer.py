import tkinter as tk
from PIL import Image,ImageTk

class imageViewer(tk.Frame):
	"""
	Used to quickly load and view an image from a local file
	created with the image's size as per ImageTk.PhotoImage().width() x ImageTk.PhotoImage().height()
	"""
	def __init__(self,parent, path= None):
		super().__init__(parent)

		self._canvas = tk.Canvas(self)
		if path is not None:
			self._img = ImageTk.PhotoImage(Image.open(path))
			self._ix = self._img.width()
			self._iy = self._img.height()
			self._canvas.config(width = self._ix, height = self._iy)
			self._canvas.create_image(20,20,anchor=tk.NW, image=self._img)
		else:
			self._iy = 0
			self._ix = 0
		self._canvas.pack()
		
	def imageSize(self):
		"""
		Returns a tuple of the size of the current image
		:return: tuple(x,y)
		"""
		x = (self._ix,self._iy)
		return x
	
	def changeImage(self, path):
		self._img = ImageTk.PhotoImage(Image.open(path))
		self._ix = self._img.width()
		self._iy = self._img.height()
		self._canvas.config(width = self._ix, height=self._iy)
		self._canvas.create_image(20, 20, anchor=tk.NW, image=self._img)
