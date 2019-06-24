"""
stagger encoding is an encoding that uses a reversible, recreatable way to distribute the message throughout the input file.

Does not support JPG due to JPGs lossy compression
"""

from src import core

class stagger:
	
	def __init__(self, imagepath):
		self._path = imagepath
		self._pixels = core.get_file_content(self._path)
	
	def encode_message(self, message, output=None):
		"""
		
		:param message:The message to encode
		:type message: str
		:param output: a string to the path for the file to be saved to, or None for it to return a list of pixels
		:type output: str
		:return:  None returned if output path specified, as image will be saved to the path. List of pixels returned if nothing provided for output
		:exception: (ValueError)
		"""
		pass
		
	
	
	def extract_message(self)->str:
		"""
		
		:return: (str) the extracted message from the image. Will be nonsensical if the image provided is not properly encoded.
		"""
		message = ""
		
		return message
		
	
	def _extract_length(self):
		"""
		
		:param pixels: (list) pixels expected to have a valid stagger.stagger-encoded image
		:type pixels: list
		:return: the expected length of the encoding. will be incorrect if the image was not encoded.
		"""
		pass


if __name__ == '__main__':
	#testing mode: this is running in place to test the module
	s = stagger("test.jpg")
	# print('This module provides utility only and should not be run by itself')
