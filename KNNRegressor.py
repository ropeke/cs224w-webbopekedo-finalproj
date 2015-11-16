import random

class KNNRegressor:
	'Regressor that takes mean of ratings for nodes above a similarity threshold'

	similarityThreshold = 0.0
	nameLabel = ''

	def __init__(self, similarityThreshold):
		self.similarityThreshold = similarityThreshold
		self.nameLabel = 'KNNRegressor'

	def predict(self, userId, businessId, similarityScores, ratings):
		similarUsers = list()
		sumOtherRatings = 0.0
		if userId in similarityScores.keys():
			for rating in ratings:
				if rating[0] == userId: continue
				for i in xrange(len(similarityScores[userId])):
					if similarityScores[userId][i][0] == rating[0] and similarityScores[userId][i][1] > self.similarityThreshold:
						similarUsers.append(rating[0])
						sumOtherRatings += rating[1]

		if len(similarUsers) == 0: return random.uniform(1, 5)
		return sumOtherRatings / len(similarUsers)




