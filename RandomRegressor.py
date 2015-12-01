"""
FILE: RandomRegressor.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

import random

class RandomRegressor:
	"""
	Regressor that guesses psuedo-random float value between provided range.
	The predicted rating of business B by user A is selected randomly from
	a uniform distribution between a given start and stop value.
	"""
	# Minimum value in uniform distribution
	rangeStart = 0
	# Maximum value in uniform distribution
	rangeStop = 0
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self, rangeStart, rangeStop):
		self.rangeStart = rangeStart
		self.rangeStop = rangeStop
		self.nameLabel = 'RandomRegressor'

	def predict(self,*unused):
		"""
		Predicts a single rating of a business B by a user A randomly.
		
		Return value:
		the predicted value of the rating of business B by user A
		"""
		return random.uniform(self.rangeStart, self.rangeStop)