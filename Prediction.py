class Prediction:

	userId = ''
	businessId = ''
	predictedValue = 0.0
	observedValue = 0.0

	def __init__(self, userId, businessId, predictedValue, observedValue):
		self.userId = userId
		self.businessId = businessId
		self.predictedValue = predictedValue
		self.observedValue = observedValue