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

from src import core
class naive:
	def __init__(self,path):
		self._path = path
		self._pixels = core.get_file_content(self._path)
	
	
	def encode_message(self,path,message, output=None):
		pixels = self._pixels
		bytestring = core.bytelist_to_string(core.string_to_ascii(message))
		excode_len = "{0:b}".format(len(bytestring))
	
		newpixels = pixels.copy()
		i=0
		try:
			while len(bytestring) > 0:
				for p in pixels:
					pix = [core.int_to_bin(x) for x in p]
					
					if len(bytestring) == 0:
						break
						
					pix[0] = list(pix[0])
					pix[0][-2:] = bytestring[0:2]
					bytestring = bytestring[2:]
			
	
					pix[1] = list(pix[1])
					pix[1][-2:] = bytestring[0:2]
	
					bytestring = bytestring[2:]
			
	
					pix[2] = list(pix[2])
					pix[2][-2:] = bytestring[0:2]
	
					bytestring = bytestring[2:]
	
					pix[0] = ''.join(pix[0])
					pix[1] = ''.join(pix[1])
					pix[2] = ''.join(pix[2])
					pix = [int(x,2) for x in pix]
					pix = tuple(pix)
					newpixels[i]=pix
					i += 1
	
	
					if len(bytestring) == 0:
						break
	
		except:
			return [False,'Unable to encode message']
			
		while len(excode_len) < 24:
			excode_len = '0'+excode_len
	
		xorbits = ''
		
		a,b,c = newpixels[0]
		a = "{0:b}".format(a)
		b = "{0:b}".format(b)
		c = "{0:b}".format(c)
		for n in [a,b,c]:
			while len(n) < 8:
				n = '0'+n
			xorbits += n
	
	
		decode_bot = (int(xorbits,2)^int(excode_len,2)) #bitwise xor
		encoded_len = '{0:b}'.format(decode_bot)
	
	
		length_pixels = [newpixels[-3],newpixels[-2],newpixels[-1]]
		i = 0
	
		for pixels in length_pixels:
			pix = [core.int_to_bin(p) for p in pixels]
			
			pix[0] = list(pix[0])
			pix[0][-2:] = encoded_len[0:2]
			pix[0] = ''.join(pix[0])
			
			encoded_len = encoded_len[2:]
			
			pix[1] = list(pix[1])
			pix[1][-2:] = encoded_len[0:2]
			pix[1] = ''.join(pix[1])
			
			encoded_len = encoded_len[2:]
	
			pix[2] = list(pix[2])
			pix[2][-2:] = encoded_len[0:2]
			pix[2] = ''.join(pix[2])
	
			encoded_len = encoded_len[2:]
			
			pix = [int(x, 2) for x in pix]
			length_pixels[i] = tuple(pix)
			i += 1
	
		r,g,b = newpixels[-4]
		_r = '{0:b}'.format(r)
		_r = list(_r)
		_r[-2:] = encoded_len
		_r = ''.join(_r)
		r = int(_r,2)
		newpixels[-4] = (r,g,b)
	
		i = 3
		for pixel in length_pixels:
			newpixels[-i] = pixel
			i -= 1
	
	
		#if you want the pixels directly and not to create an output, set output to '', False or None
		if output != '' and output != False and output is not None:
			core.put_file_content(newpixels, output, core.imsize(path))
	
		return [True,newpixels]


	def extract_message(self):
		
	
		pixels = self._pixels
	
		bitstream = ''
		length = self._extract_length(pixels)
	
		for p in pixels[0:length]:
			#this 0:length will overshoot the number of pixels required. I need to cut this down. need to find what divisor to use that will minimally overshoot
			#at the minimum, it will stop it decoding every pixel, which takes a long time.
			for c in p:
				c = core.int_to_bin(c)
				p = c[-2:]
				bitstream += p
	
		bs = bitstream[0:int(length)]
	
		asc = core.bin2asc(bs)
		return ''.join(asc)
	
	
	def _extract_length(self):
		"""
	
		:param pixels: (list) pixels expected to have a valid stagger.naive-encoded image
		:return: the expected length of the encoding. will be incorrect if the image was not encoded.
		"""
		pixels = self._pixels
		
		length_pixels = [pixels[-3],pixels[-2], pixels[-1]]
		bitstring = ''
	
		for p in length_pixels:
			r,g,b = p
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

if __name__ == '__main__':
	print('This module provides utility only and should not be run by itself')
