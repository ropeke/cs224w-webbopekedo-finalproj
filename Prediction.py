"""
FILE: Prediction.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

class Prediction:
	"""
	Prediciton class useful for making instances of predicitons.
	Stores predicted rating of business B by user A, and the observed rating.
	"""

	# id of user A
	userId = ''
	# id of business B
	businessId = ''
	# predicted rating
	predictedValue = 0.0
	# observed (actual) rating
	observedValue = 0.0

	def __init__(self, userId, businessId, predictedValue, observedValue):
		self.userId = userId
		self.businessId = businessId
		self.predictedValue = predictedValue
		self.observedValue = observedValue