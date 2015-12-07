"""
FILE: KNNRegressor.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

import random

class KNNRegressor:
	"""
	Variation on standard KNN regression. The predicted rating of a business B
	by a user A is equal to the sum of the observed ratings of all users that also
	rated B, each scaled by their similarity score to user A (similarity should be in [0,1]),
	divided by the sum of those similarity scores.
	"""

	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self):
		self.nameLabel = 'KNNRegressor'

	# TODO: Change so that a neighbor's vote is scaled by its similarity score
	def predict(self, userId, businessId, similarityScores, ratings):
		"""
		Predicts a single rating of a business B by a user A using weighted kNN regression.

		Keyword arguments:
		userId           -- id of user A, needed to access similarity score and rating
		businessId       -- id of business B, needed to access rating
		similarityScores -- map of user id -> list of (user id of similar user, similarity score) tuples
		ratings          -- map of business id -> list of (user id of user that rated business, rating) tuples
		
		Return value:
		the predicted value of the rating of business B by user A
		"""
		# Running total of observed ratings scaled by similarity score with user A
		neighborVotes = 0.0
		# Running total of similarity scores
		relevantSimilarities = 0.0
		if userId in similarityScores.keys():
			for rating in ratings:
				if rating[0] == userId: continue # can't use the observed value
				# Loop through all users that user A has a similarity score with
				for i in xrange(len(similarityScores[userId])):
					# Similar user actually rated buseiness B
					if similarityScores[userId][i][0] == rating[0]: 
						# Scale observed rating by similarity score
						neighborVotes += rating[1]*similarityScores[userId][i][1]
						relevantSimilarities += similarityScores[userId][i][1]

		# If no similar users to compare to, guess randomly
		# if relevantSimilarities == 0: return random.uniform(1, 5)
		if relevantSimilarities == 0: return 0

		return neighborVotes / relevantSimilarities




