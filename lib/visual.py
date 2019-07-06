from lib import core
from PIL import Image

def redback(original: str,secondary: str, outputfile: str):
	"""

	Creates an image that is all red except for pixels that are different between the original and secondary files, which are greyscaled based on their colour chanel difference
	Not very useful if there is noise added in postprocessing.
	:param original :(str) Path to the original file
	:param secondary: (str) Path to the second file
	:param outputfile: (str) Path for the output (difference) to save to.
	:return: Void
	"""
	originalpath = original
	original = core.get_file_content(original)
	secondary = core.get_file_content(secondary)

	i = 0
	dif = []
	for pixel in original:
		r1,g1,b1 = pixel
		r2,g2,b2 = secondary[i]

		r3 = abs(r1-r2)
		g3 = abs(g1-g2)
		b3 = abs(b1-b2)

		if r3 != 0 or g3 != 0 or b3 != 0:
			dif.append((r3*5,g3*5,b3*5))
		else:
			dif.append((255,0,0))

		i+=1


	im = Image.open(originalpath)
	size = im.size
	img2 = Image.new('RGB', size, 'white')
	img2.putdata(dif)
	img2.save(outputfile)
	
