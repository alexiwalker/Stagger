"""
stagger encoding is an encoding that uses a reversible, recreatable way to distribute the message throughout the input file.

Does not support JPG due to JPGs lossy compression
"""

from src import core
import random

lsb_random = ['00', '01', '10', '11']


class Stagger:
	
	def __init__(self, imcontents):
		if type(imcontents) == str:
			self._path = imcontents
			self._pixels = core.get_file_content(self._path)
		
		
		elif type(imcontents) == list:
			self._pixels = imcontents
	
	def encode_message(self, message, output=None):
		"""
		
		:param message:The message to encode
		:type message: str
		:param output: a string to the path for the file to be saved to, or None for it to return a list of pixels
		:type output: str
		:return:  None returned if output path specified, as image will be saved to the path. List of pixels returned if nothing provided for output
		:exception: (ValueError)
		"""
		if (len(self._pixels) // 63) - 6 < len(message):
			raise ValueError(f"Message too long. "
			                 f"This image can only encode a message with a length of {(len(self._pixels) // 63) - 12} ")
		
		pixels = self._pixels
		newPixels = self._pixels.copy()
		
		messageBinary = core.string_to_ascii(message)
		messageBinary = ''.join(messageBinary)
		messageBinary += core.NULLBYTE
		i = 0
		messagePixels = []
		
		while len(messageBinary) > 0:
			pixel = pixels[i]
			r, g, b = pixel
			
			b_pixel = [core.int_to_bin(x) for x in pixel]
			bpo = b_pixel.copy()
			
			# pixels are read in order r,g,b
			b_pixel[0] = list(b_pixel[0])
			b_pixel[0][-2:] = messageBinary[0:2]
			messageBinary = messageBinary[2:]
			b_pixel[0] = ''.join(b_pixel[0])
			
			if len(b_pixel[0]) < 8:
				b_pixel[0] = bpo[0]
				raise ValueError('fatal error while encoding')
			
			b_pixel[1] = list(b_pixel[1])
			b_pixel[1][-2:] = messageBinary[0:2]
			messageBinary = messageBinary[2:]
			b_pixel[1] = ''.join(b_pixel[1])
			
			# if one channel is not used for the pixel (ie, the str gets replaced as empty) then the pixel becomes the original value
			if len(b_pixel[1]) < 8:
				b_pixel[1] = bpo[1]
			
			b_pixel[2] = list(b_pixel[2])
			b_pixel[2][-2:] = messageBinary[0:2]
			messageBinary = messageBinary[2:]
			b_pixel[2] = ''.join(b_pixel[2])
			
			if len(b_pixel[2]) < 8:
				b_pixel[2] = bpo[2]
			
			newPixel = [int(x, 2) for x in b_pixel]
			newPixel = tuple(newPixel)
			
			newPixels[i] = newPixel
			messagePixels.append(i)
			i += self._jump_length(r)
		
		#Randomise 2 LSB of every pixel not used to store the message, to mess with visual attacks
		index = 0
		for pixel in newPixels:
			if index not in messagePixels:
				r,g,b = pixel
				r = core.int_to_bin(r)
				g = core.int_to_bin(g)
				b = core.int_to_bin(b)

				r = list(r)
				g = list(g)
				b = list(b)

				r[-2:] = lsb_random[random.randint(0,3)]
				g[-2:] = lsb_random[random.randint(0,3)]
				b[-2:] = lsb_random[random.randint(0,3)]

				r = ''.join(r)
				g = ''.join(g)
				b = ''.join(b)

				r = core.bin_to_int(r)
				g = core.bin_to_int(g)
				b = core.bin_to_int(b)

				p = (r,g,b)
				newPixels[index] = p
			index+=1
		
		if output != '' and output != False and output is not None:
			core.put_file_content(newPixels, output, core.imsize(self._path))
		
		if not output:
			return [True, newPixels]
	
	@staticmethod
	def _jump_length(r):
		r_ = core.int_to_bin(r)
		r_ = r_[0:6]
		r_ = core.bin_to_int(r_)
		r_ += 1
		return r_
	
	def extract_message(self) -> str:
		"""
		
		:return: (str) the extracted message from the image. Will be nonsensical if the image provided is not properly encoded.
		"""
		i = 0
		pixels = self._pixels
		buffer = ['']
		buffer8 = ''
		try:
			while True:
				pixel = pixels[i]
				r, g, b = pixel
				pixel_jump = self._jump_length(r)
				
				p = [core.int_to_bin(x) for x in pixel]
				for b in p:
					if len(buffer8) < 8:
						buffer8 += b[-2:]
					else:
						if buffer8 == core.NULLBYTE:
							raise core.LevelBreak('NULLBYTE')
						buffer.append(buffer8)
						buffer8 = b[-2:]
				
				if i > len(pixels):
					raise ValueError('Message could not be extracted: Null byte not found')
				i += pixel_jump
		
		except core.LevelBreak:
			pass
		
		message = ''.join(buffer)
		message = core.text_from_bits(message)
		return message
	
	def _extract_length(self):
		"""
		
		:param pixels: (list) pixels expected to have a valid stagger.stagger-encoded image
		:type pixels: list
		:return: the expected length of the encoding. will be incorrect if the image was not encoded.
		"""
		pass


if __name__ == '__main__':
	print('This module provides utility only and should not be run by itself')
