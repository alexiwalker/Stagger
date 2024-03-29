if __name__ == '__main__':
	raise NameError("Module does not support being run as '__main__'")

import binascii
import random

"""
Core contains generic helper functions
They are used by the encoding files
saving images from modified pixels,

"""
class LevelBreak(Exception):
	pass

from PIL import Image

NULLBYTE = '00000000'

def encoding_types():
	return [
		'Stagger',
		'Linear'
	]

def int_to_bin(n):
	"""
	converts an int to a string of binary with a minimum of 8 bytes (leading 0s) eg  2 -> 00000010
	:param n: Integer to convert to binary
	:return: str
	"""
	_bin = '{0:b}'.format(n)
	while len(_bin) < 8:
		_bin = '0' + _bin
	
	return _bin


def bitstream_to_8bit(binary):
	"""
	chunks a string into 8 character chunks in a list. Final entry in the list may not be len() == 8
	Used to turn a string of binary into its individual bytes
	:param binary:
	:type binary: str
	:return: list
	"""
	_bytes = []
	while binary != '':
		_bytes.append(binary[0:8])
		binary = binary[8:]

	return _bytes


def get_file_content(image):
	"""
	Takes a file path to an image and returns a list of its pixels
	:param image: path to the image
	:type image: str
	:return: list
	"""
	im = Image.open(image)
	pixels = list(im.getdata())
	return pixels


def put_file_content(pixels, path, size):
	"""
	Saves list of pixels to a file. file type determined by the extensions in the file path provided
	:param pixels: List if pixels each being a tuple (int,int,int)
	:param path: path to save the file to
	:param size: tuple of (w,h) that is the size of the image
	:return: None
	"""
	img = Image.new('RGB', size, 'white')
	img.putdata(pixels)
	img.save(path)


def string_to_ascii(string):
	"""
	Converts a string to binary according to the ascii encoding
	:param string: the string to be converted
	:return: list of bytes for each character in the string
	"""
	asc = string.encode('ascii')
	
	bytelist = []
	for a in asc:
		a = '{0:b}'.format(a)
		while len(a) < 8:
			a = '0' + a
		bytelist.append(a)
	
	return bytelist


def bin_to_int(_bin):
	"""
	Converts binary string to int
	:param _bin: binary string
	:return: int
	"""
	return int(_bin, 2)


def bytelist_to_string(bytelist):
	"""
	turns a list of bytes into a string
	todo why do i even have this function when ''.join() is a thing? I can probably just replace this or cut it.
	:param bytelist:
	:return:
	"""

	bytestring = ''
	for b in bytelist:
		bytestring = bytestring + b + ''
	return bytestring


def image_size(path):
	"""
	Gets size of image tuple(int,int) based on the path provided
	:param path:
	:type path: str
	:return: tuple(int,int)
	"""
	im = Image.open(path)
	return im.size


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
	"""

	:param bits: string of binary that is to be converted to a string of ascii characters
	:param encoding: overritable encoding. defaults to utf-8. probably don't change this
	:param errors: ? Just using the params I saw in original docs
	:return: string of ascii characters
	"""
	n = int(bits, 2)
	return int_to_bytes(n).decode(encoding, errors)


def int_to_bytes(i):
	hex_string = '%x' % i
	n = len(hex_string)
	return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def bin_to_ascii(binary):
	_bytes = []
	while binary != '':
		_bytes.append(binary[0:8])
		binary = binary[8:]
	return _bytes


def noise_image(path, size):
	"""
	This is a bit slow. Generate a noisy image to test encoding on without needing an existing image
	:param path: path to save the image to
	:type path: str
	:param size:
	:type size: tuple
	:return: None
	"""
	if type(size) is not tuple:
		raise TypeError
	
	x, y = size
	n = x * y
	pixels = []
	for p in range(n):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		pixels.append((r, g, b))
	
	put_file_content(pixels, path, size)


class Protocol:

	def __init__(self):
		pass

	def encode_message(self, message, output=None):
		raise NotImplementedError

	def extract_message(self):
		raise NotImplementedError

	def message_maximum_length(self):
		raise NotImplementedError