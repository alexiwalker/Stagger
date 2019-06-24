import binascii


"""
Core contains generic helper functions
They are used by the encoding files
saving images from modified pixels,

"""
from PIL import Image


def int_to_bin(n):
	bin = '{0:b}'.format(n)
	while len(bin) < 8:
		bin = '0' + bin

	return bin


def bitstream_to_8bit(binary):
	bytes = []
	while binary != '':
		bytes.append(binary[0:9])
		binary = binary[9:]
	return bytes


def get_file_content(image):
	im = Image.open(image)
	pixels = list(im.getdata())
	return pixels


def put_file_content(pixels, path, size):
	img = Image.new('RGB', size, 'white')
	img.putdata(pixels)
	img.save(path)


def string_to_ascii(string):
	asc = string.encode('ascii')

	bytelist = []
	for a in asc:
		a = '{0:b}'.format(a)
		while len(a) < 8:
			a = '0' + a
		bytelist.append(a)

	return bytelist


def bin_to_int(bin):
	return int(bin, 2)

def bytelist_to_string(bytelist):
	bytestring = ''
	for b in bytelist:
		bytestring = bytestring + b + ''
	return bytestring

def imsize(path):
	im = Image.open(path)
	print(im.size)
	return im.size

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
	n = int(bits, 2)
	return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
	hex_string = '%x' % i
	n = len(hex_string)
	return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def bin2asc(binary):
	bytes = []
	while binary != '':
		bytes.append(binary[0:8])
		binary = binary[8:]
	return bytes

