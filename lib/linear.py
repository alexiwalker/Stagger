"""

Naive is a low quality way to encode string of text into an image

it uses last 2 bits of each colour chanel per pixel to encode ascii binary. It applies them all sequentially.

The last few pixels of the image encode the length of the string as above, but XORed with the binary of the first pixel

it pulls out bits from the string until the string is length decoded from above

The resulting information is then decoded from 8bit binary to ascii (7bit, left  0 pad)

Do not use this method. It is easily visibile to difference / visual attacks (see redback visual attack module)

Does not work on jpegs due to compression causing artifacting and damaging pixel integrity.

PNG does work. Other filetypes unteste

"""

from lib import core


class Linear(core.Protocol):
	def __init__(self, imcontents):

		super(Linear, self).__init__()
		if type(imcontents) == str:
			self._path = imcontents
			self._pixels = core.get_file_content(self._path)
		
		
		elif type(imcontents) == list:
			self._pixels = imcontents
	
	def encode_message(self, message, output=None):
		pixels = self._pixels
		newPixels = pixels.copy()
		messageBinary = ''.join(core.string_to_ascii(message))
		messageBinary += core.NULLBYTE
		
		i = 0
		while len(messageBinary) > 0:
			for pixel in pixels:
				
				binaryPixel = [core.int_to_bin(x) for x in pixel]
				
				# pixels are read in order r,g,b

				newPixel, messageBinary = self._encode_pixel(binaryPixel, messageBinary)
				
				newPixels[i] = newPixel
				
				i += 1
				if len(messageBinary) == 0:
					break
		
		if output != '' and output != False and output is not None:
			core.put_file_content(newPixels, output, core.image_size(self._path))
		
		if not output:
			return [True, newPixels]
		
	@staticmethod
	def _encode_pixel(binaryPixel, messageBinary):
		originalBinaryPixel = binaryPixel.copy()
		
		binaryPixel[0] = list(binaryPixel[0])
		binaryPixel[0][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[0] = ''.join(binaryPixel[0])
		
		if len(binaryPixel[0]) < 8:
			binaryPixel[0] = originalBinaryPixel[0]
			print('fatal error while encoding: nothing to encode')
			raise ValueError
		
		binaryPixel[1] = list(binaryPixel[1])
		binaryPixel[1][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[1] = ''.join(binaryPixel[1])
		
		# if one channel is not used for the pixel (ie, the str gets replaced as empty) then the pixel becomes the original value
		if len(binaryPixel[1]) < 8:
			binaryPixel[1] = originalBinaryPixel[1]
		
		binaryPixel[2] = list(binaryPixel[2])
		binaryPixel[2][-2:] = messageBinary[0:2]
		messageBinary = messageBinary[2:]
		binaryPixel[2] = ''.join(binaryPixel[2])
		
		if len(binaryPixel[2]) < 8:
			binaryPixel[2] = originalBinaryPixel[2]
		
		newPixel = [int(x, 2) for x in binaryPixel]
		newPixel = tuple(newPixel)
		
		return newPixel, messageBinary
	
	def extract_message(self):
		
		pixels = self._pixels
		buffer = ['']
		buffer8 = ''
		
		try:
			for pixel in pixels:
				pixel = list(pixel)
				p = [core.int_to_bin(x) for x in pixel]
				
				for b in p:
					if len(buffer8) < 8:
						buffer8 += b[-2:]
					else:
						if buffer8 == core.NULLBYTE:
							raise core.LevelBreak('NULLBYTE')
						buffer.append(buffer8)
						buffer8 = b[-2:]
		except core.LevelBreak:
			pass
	
		
		messageBinary = ''.join(buffer)
		
		Message = core.text_from_bits(messageBinary)
		return Message


	def _extract_length(self,pixels = None):
		"""
		This method was from a previous implementation where I XOR'd the LSBs of last 3 pixels with the first pixel to give a length so i can cut right at the point
		
		this is no longer used since the reimplementation of naive to use a NULLBYTE terminator.
		
		It is being kept for future reference
		
		This may be reused for a different encoding, and as such is being left in
		:param pixels: (list) pixels expected to have a valid stagger.naive-encoded image
		:return: the expected length of the encoding. will be incorrect if the image was not encoded.
		"""
		
		if pixels is not None:
			pixels = self._pixels
		
		length_pixels = [pixels[-3], pixels[-2], pixels[-1]]
		bitstring = ''
		
		for p in length_pixels:
			r, g, b = p
			bitstring += '{0:b}'.format(r)[-2::]
			bitstring += '{0:b}'.format(g)[-2::]
			bitstring += '{0:b}'.format(b)[-2::]
		
		xorbits = ''
		
		a, b, c = pixels[0]
		a = "{0:b}".format(a)
		b = "{0:b}".format(b)
		c = "{0:b}".format(c)
		for n in [a, b, c]:
			while len(n) < 8:
				n = '0' + n
			xorbits += n
		
		last_2 = pixels[-4]
		_p = core.int_to_bin(last_2[0])
		l2 = _p[-2:]
		
		bitstring = bitstring + l2
		
		length = (int(xorbits, 2) ^ int(bitstring, 2))
		
		return length

	def message_maximum_length(self):
		return (6*len(self._pixels))//8

if __name__ == '__main__':
	print('This module provides utility only and should not be run by itself')
