import pymprog as mp
import numpy
import scipy.stats as stats


class IP:
	
	def __init__(self, constraints=True):
		self.constraints = constraints
		
	def predict(self, c, unknown):
		if c.size < 2:
			return []
		
		addedElems = 0
		if c.shape[1]-c.shape[0]>1:
			added = numpy.zeros((c.shape[1]-c.shape[0], c.shape[1]))
			addedElems = added.shape[0] * added.shape[1]
			c = numpy.vstack((c, added))

		detected = c.shape[0]
		recognizers = c.shape[1]
		size = c.size
		
		mp.beginModel('basic')
		mp.verbose(False)
		x = mp.var(range(size), 'X', kind=bool)
		

		# One label per detected object
		for i in range(0, detected):
			tmp = numpy.zeros((detected, recognizers))
			tmp[i, :] = 1
			tmp = tmp.reshape((1, size))[0]
			mp.st(sum(x[j]*int(tmp[j]) for j in range(size))==1)

		if self.constraints == True:
			# Use recognizer up to once
			if unknown==True:
				lim = recognizers-1
			else:
				lim = recognizers
			for i in range(0, recognizers):
				tmp = numpy.zeros((detected, recognizers))
				tmp[:, i] = 1
				tmp = tmp.reshape((1, size))[0]
				mp.st(sum(x[j]*int(tmp[j]) for j in range(size))<=1)
			
		c = c.reshape((1, size)).tolist()[0]
			
		mp.minimize(sum(c[i]*x[i] for i in range(size)), 'myobj')
		mp.solve(int)
		
		X = numpy.zeros((1, size))
		for i in range(size):
			X[0, i] = x[i].primal
		X = X[0,0:size-addedElems]

		labels = X.reshape(((size-addedElems)/(recognizers), recognizers))
		predicted = []
		for i in range(0, labels.shape[0]):
			l = numpy.argmax(labels[i,:])
			if l==recognizers-1 and unknown==True:
				l = -1
			predicted.append(l)
			
		return predicted