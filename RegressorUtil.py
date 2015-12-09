"""
FILE: RegressorUtil.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

import math
from Prediction import Prediction
import numpy as np

def getAveragePrediction(allPredictions, businessId, userId):
	numVotes = 0.0
	sumVotes = 0.0
	for predictionSet in allPredictions:
		for prediction in predictionSet:
			if prediction.businessId == businessId and prediction.userId == userId:
				sumVotes = sumVotes + prediction.predictedValue
				numVotes = numVotes + 1

	if numVotes == 0: return 0
	return sumVotes / numVotes

def averagePredictions(allPredictions, businessToRaters):
	averagePredicts = list()
	print 'Total Businesses:', len(businessToRaters.keys())
	counter = 1
	possiblePredictionsCounter = 0.0
	for businessId in businessToRaters.keys():
		print 'Currently on business', counter
		ratings = businessToRaters[businessId]
		# Predict rating for each user based on similarity
		for i in range(len(ratings)):
			userId = ratings[i][0]
			predictedValue = getAveragePrediction(allPredictions, businessId, userId)
			possiblePredictionsCounter = possiblePredictionsCounter + 1
			if predictedValue == 0: continue
			observedValue = ratings[i][1]
			prediction = Prediction(userId, businessId, predictedValue, observedValue)
			predictions.append(prediction)

		counter += 1
	print "Number of possible predictions:", possiblePredictionsCounter
	print "Number of predictions actually made:", len(predictions)
	print "Fraction of predictions made:", float(len(predictions))/possiblePredictionsCounter
	return predictions

def runRegressor(similarityScores, businessToRaters, predictor):
	"""
	Runs all trials of the regressor, predicting a rating for every
	business-user pair. Note that ratings are only predicted for
	instances where a user actually rated the business.

	Keyword arguments:
	similarityScores -- map of user id -> list of (user id of similar user, similarity score) tuples
	businessToRaters -- map of business id -> list of (user id of user that rated business, rating) tuples
	predictor        -- prediction (regression) model

	Return value:
	a list of Prediction objects for each business-user pair
	"""

	# Final result storing all prediction objects, will be used to evaluate results
	predictions = list()

	# Loop through each business, and predict rating by each user
	print 'Total Businesses:', len(businessToRaters.keys())
	counter = 1
	possiblePredictionsCounter = 0.0
	for businessId in businessToRaters.keys():
		print 'Currently on business', counter
		ratings = businessToRaters[businessId]
		# Predict rating for each user based on similarity
		for i in range(len(ratings)):
			userId = ratings[i][0]
			if userId not in similarityScores.keys(): continue
			predictedValue = predictor.predict(userId, businessId, similarityScores, ratings)
			possiblePredictionsCounter = possiblePredictionsCounter + 1
			if predictedValue == 0: continue
			observedValue = ratings[i][1]
			prediction = Prediction(userId, businessId, predictedValue, observedValue)
			predictions.append(prediction)

		counter += 1
	print "Number of possible predictions:", possiblePredictionsCounter
	print "Number of predictions actually made:", len(predictions)
	print "Fraction of predictions made:", float(len(predictions))/possiblePredictionsCounter
	return predictions

def evaluateRegressor(predictions, predictorLabel, similarityMeasureLabel):
	"""
	Evaluates the accuracy of the predictions and reports error statistics.

	Keyword arguments:
	predictions       -- a list of Prediction objects for each business-user pair
	predictor         -- prediction (regression) model
	similarityMeasure -- the selected similarity measure used in predictions

	"""
	# Evaluate system with error metrics

	errorSquareSum = 0.0
	errorHistogram = dict.fromkeys(range(-4,5),0)
	confusionMatrix = np.zeros((5, 5))

	for predict in predictions:
		error = predict.predictedValue - predict.observedValue
		errorHistogram[int(round(error))] += 1
		errorSquareSum += math.pow(error, 2)
		roundPredict = int(round(predict.predictedValue))
		roundObserved = int(round(predict.observedValue))
		confusionMatrix[roundPredict-1, roundObserved-1] += 1


	meanSquareError = errorSquareSum / len(predictions)
	l2Error = math.sqrt(errorSquareSum)


	# Print error metrics
	print '###############################'
	print '#       ERROR ANALYSIS        #'
	print '###############################'
	print 'Similarity Measure:', similarityMeasureLabel
	print 'Predictor:', predictorLabel
	print 'Mean Square Error =', meanSquareError
	print 'L2 Error =', l2Error
	print 'Error Histogram (prediction - observed):'
	print 'Error', '\tCount'
	for i in range(-4,5):
		print i, '\t', errorHistogram[i]
	print 'Confusion Matrix (predicted rows[1:5], observed cols[1:5]):'
	print '\t1\t2\t3\t4\t5'
	for i in range(5):
		rowString = str(i+1)
		for j in range(5):
			rowString += '\t' + str(int(confusionMatrix[i,j]))
		print rowString


