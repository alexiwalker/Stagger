from src import linear, core, stagger, visual
import os

#src is symlinked from the main src folder for ease of use

TEST_MESSAGE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 the quick brown fox Jumped over the lazy dog'

class test:
	"""
	todo implement a testrunner for the different encodes/decodes and core functions
	"""
	
	@staticmethod
	def Linear():
		if not os.path.exists("images/test.png"):
			core.noise_image("images/test.png", (1920,1080))
			
		n = linear.Linear("images/test.png")
		px = n.encode_message(TEST_MESSAGE)
		assert (px[0] and linear.Linear(px[1]).extract_message() == TEST_MESSAGE)
		
		print('linear.Linear OK')
		
	@staticmethod
	def Stagger():
		if not os.path.exists("images/test.png"):
			core.noise_image("images/test.png", (1920,1080))
		
		n = stagger.Stagger("images/test.png")
		px = n.encode_message(TEST_MESSAGE)

		assert (px[0] and stagger.Stagger(px[1]).extract_message() == TEST_MESSAGE)
		
		print('stagger.Stagger OK')


if __name__ == '__main__':
	test.Linear()
	test.Stagger()

	
	
	
	

