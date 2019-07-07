from lib import linear, core, stagger, visual
import os

# lib is symlinked from the main lib folder for ease of use

TEST_MESSAGE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 the quick brown fox Jumped over the lazy dog'

BASE_IMAGE = "images/test.png"

class test:

	@staticmethod
	def Linear():
		if not os.path.exists(BASE_IMAGE):
			core.noise_image(BASE_IMAGE, (1920, 1080))
		
		n = linear.Linear(BASE_IMAGE)
		px = n.encode_message(TEST_MESSAGE)
		
		assert px[0]
		assert linear.Linear(px[1]).extract_message() == TEST_MESSAGE
		
		print('linear.Linear OK')
	
	@staticmethod
	def Stagger():
		if not os.path.exists(BASE_IMAGE):
			core.noise_image(BASE_IMAGE, (1920, 1080))
		
		n = stagger.Stagger(BASE_IMAGE)
		px = n.encode_message(TEST_MESSAGE)
		
		assert px[0]
		assert stagger.Stagger(px[1]).extract_message() == TEST_MESSAGE
		
		print('stagger.Stagger OK')


if __name__ == '__main__':
	test.Linear()
	test.Stagger()
