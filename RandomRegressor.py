import random

class RandomRegressor:
	'Regressor that guesses psuedo-random float value between provided range'

	rangeStart = 0
	rangeStop = 0
	nameLabel = ''

	def __init__(self, rangeStart, rangeStop):
		self.rangeStart = rangeStart
		self.rangeStop = rangeStop
		self.nameLabel = 'RandomRegressor'

	def predict(self,*unused):
		return random.uniform(self.rangeStart, self.rangeStop)