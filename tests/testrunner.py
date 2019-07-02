from src import naive, core
import os
#src is symlinked from the main src folder for ease of use

TEST_MESSAGE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 the quick brown fox Jumped over the lazy dog'

class test:
	"""
	todo implement a testrunner for the different encodes/decodes and core functions
	"""
	
	@staticmethod
	def Naive():
		if not os.path.exists("images/test.png"):
			core.noise_image("images/test.png", (1920,1080))
			
		n = naive.Naive("images/test.png")
		px = n.encode_message(TEST_MESSAGE)
		assert (px[0] and naive.Naive(px[1]).extract_message() == TEST_MESSAGE)
		
		


if __name__ == '__main__':
	test.Naive()

