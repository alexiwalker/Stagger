"""
stagger encoding is an encoding that uses a reversible, recreatable way to distribute the message throughout the input file.

Does not support JPG due to JPGs lossy compression
"""

from lib import core
import random

lsb_random = ['00', '01', '10', '11']

class Stagger(core.Protocol):
	
	def __init__(self, imcontents, skip_noise = False):
		"""
				:param imcontents: The image to be used as the base to encode from
				:type imcontents: list or str
				:param skip_noise: Noise LSB of pixels not required for the encoding. Protects against raw visual attacks but increases encode time.
				:type skip_noise: bool
		"""

		self._skip_noise = skip_noise
		super(Stagger, self).__init__()
		if type(imcontents) == str:
			self._path = imcontents
			self._pixels = core.get_file_content(self._path)
		
		
		elif type(imcontents) == list:
			self._pixels = imcontents
			
	@staticmethod
	def _encode_pixel(binaryPixel, messageBinary):
		binaryPixelOriginal = binaryPixel.copy()
		
		# pixels are read in order r,g,b
		binaryPixel[0] = list(binaryPixel[0])
		binaryPixel[0][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[0] = ''.join(binaryPixel[0])
		
		if len(binaryPixel[0]) < 8:
			binaryPixel[0] = binaryPixelOriginal[0]
			raise ValueError('fatal error while encoding')
		
		binaryPixel[1] = list(binaryPixel[1])
		binaryPixel[1][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[1] = ''.join(binaryPixel[1])
		
		# if one channel is not used for the pixel (ie, the str gets replaced as empty) then the pixel becomes the original value
		if len(binaryPixel[1]) < 8:
			binaryPixel[1] = binaryPixelOriginal[1]
		
		binaryPixel[2] = list(binaryPixel[2])
		binaryPixel[2][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[2] = ''.join(binaryPixel[2])
		
		if len(binaryPixel[2]) < 8:
			binaryPixel[2] = binaryPixelOriginal[2]
		
		newPixel = [int(x, 2) for x in binaryPixel]
		newPixel = tuple(newPixel)
		
		return newPixel, messageBinary
	
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
			
			binaryPixel = [core.int_to_bin(x) for x in pixel]
			
			newPixel, messageBinary = self._encode_pixel(binaryPixel, messageBinary)
			
			newPixels[i] = newPixel
			messagePixels.append(i)
			i += self._jump_length(pixel[0])
		
		#Randomise 2 LSB of every pixel not used to store the message, to mess with visual attacks
		# >core.redback will show some pixels as unmodified,
		# >as just by luck the rng will give some pixels the same 2 LSB on all 3 channels
		# >this is fine.
		
		index = 0

		if not self._skip_noise:
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
			core.put_file_content(newPixels, output, core.image_size(self._path))
		
		if not output:
			return [True, newPixels]
	
	@staticmethod
	def _jump_length(r) -> int:
		"""
		Calculates the 8bit binary of the integer given (0-255) and uses the first 6 digits of it (unaffected by LSB modifications
		to calculate the number of pixels forward to jump. +1.
		This means up to 64 pixels can be skipped at once
		for a 1920x1080 image, 32400 pixels may be used
		((1920*1080 image)/64 pixels available )*6 bits per image)/8 bits per character = maximum length of 24300 character message
		:param r: int
		:return: int
		"""
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

		assert type(message) == str
		return message
	

if __name__ == '__main__':
	print('This module provides utility only and should not be run by itself')
