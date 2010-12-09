import cv
import threading
import time
from BaseDetector import *
from HaarDetector import *

class ThreadedDetector:	
	def __init__(self, config):
		self.past = []
		self.config = config
		
		self.haar = HaarDetector(config.HaarCascade, config.HaarSize)
		self.haarResult = None
		self.thread = None
		
	def detect(self, image):
		res = None
		#return self.haar.detect(image)
		if len(self.past) == 0:
			res = self.haar.detect(image)
		else:
			if self.thread == None or self.thread.is_alive()==False:
				if self.haarResult != None:
					print 'Previous'
					res = self.haarResult
					self.haarResult = None
				self.image = cv.CloneImage(image)
				self.thread = threading.Thread(target=ThreadedDetector.doThreadedHaar, args=(self, image))
				self.thread.daemon = True
				self.thread.start()
			if res == None:
				res = self.past[len(self.past)-1]
		print 'Going on'	
		self.past.append(res)
		return res

	def doThreadedHaar(self, image):
		print 'Haar start'
		self.haarResult = self.haar.detect(self.image)
		print 'Haar end'
		#return self.haarResult