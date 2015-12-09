"""
FILE: RunYelpPredictor.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

import sys
import yelp_json_parser
from RandomRegressor import RandomRegressor
from KNNRegressor import KNNRegressor
import RegressorUtil
from FriendshipOverlapSimilarity import FriendshipOverlapSimilarity
from CommunitySimilarity import CommunitySimilarity
from CommuteTimeSimilarity import CommuteTimeSimilarity
from PageRankSimilarity import PageRankSimilarity
from FeatureDistanceSimilarity import FeatureDistanceSimilarity
from FeatureFactory import *

# Valid values for arguments
similarityMeasureStrings = ['foverlap','community','commute','pagerank','featureDist','all']
predicitonModelStrings = ['baseline','knn']

def printArgsHelp():
	print '#arg_name#\t\t\t#arg_value#\t\t\t#arg_description#'
	print '(optional) help:\t\t[help]\t\t\t\tprints argument instructions for RunYelpPredictor and exits'
	print 'similarityMeasure:\t\t[foverlap, community, commute, pagerank, featureDist]\t\t\tcalculates similarity between nodes using this measurment'
	print 'predictionModel:\t\t[baseline, knn]\t\t\tmodel for predicting ratings'
	print 'trials:\t\t\t\t[0 to totalTrials]\t\tinteger number of trial results to print (default 0)'
	print '(optional) buildClean:\t\t[clean]\t\t\t\trepopulates globals from json files otherwise loads from .bin (default False)'


"""
This script will run the entire prediction pipeline in __ major parts:
(Part 0): Load all relevant network information from provided Json files
Part 1: Generate similarity scores from network data
Part 2: Run prediction model
Part 3: Evaluate results

Run with parameters in this order:
-(optional) help: 		[help]							--	prints argument instructions for
															RunYelpPredictor and exits
-similarityMeasure: 	[foverlap, community, commute, pagerank, featureDist] 	-- 	calculates similarity between nodes
															using this measurment
-predictionModel: 		[baseline, knn]					--	model for predicting ratings
-trials: 				[0 to totalTrials]				--	integer number of trial results to print
-(optional) buildClean:	[clean]							--	repopulates globals from json files
															otherwise loads from .bin
"""
def main(argv):
	# Set default values
	similarityMeasure = None
	predictionModel = None
	numTrials = 0
	buildClean = False

	# Check for 'help' argument
	if argv[1] == 'help':
		printArgsHelp()
		sys.exit(0)

	# Check for valid arguments
	if len(argv) < 4:
		sys.stderr.write('Too few arguments! Try running with the \'help\' argument.\n')
		sys.exit(1)
	if argv[1] not in similarityMeasureStrings:
		sys.err.write('Invalid similarity measure! Try running with the \'help\' argument.\n')
		sys.exit(1)
	if argv[2] not in predicitonModelStrings:
		sys.err.write('Invalid prediction model! Try running with the \'help\' argument.\n')
		sys.exit(1)
	try:
		numTrials = int(argv[3])
	except ValueError:
		sys.err.write('Please provide int value for \'trials\' argument. Try running with the \'help\' argument.\n')
		sys.exit(1)
	if int(argv[3]) < 0:
		sys.err.write('Invalid integer for \'trials\'! Try running with the \'help\' argument.\n')
		sys.exit(1)
	if len(argv) > 4 and argv[4] != 'clean':
		sys.err.write('Invalid value for buildClean! Try running with the \'help\' argument.\n')
		sys.exit(1)

	if len(argv) > 4 and argv[4] == 'clean':
		buildClean = True

	# Generate Yelp data either
	# by parsing Jsons or loading from .bins

	# yelpData currently contains:
	# a map from user -> friends
	# a map from business -> users who rated that business
	# TODO: expand what yelp data contains as necessary for other sim measures
	if buildClean:
		yelpData = yelp_json_parser.parseJsons()
	else:
		yelpData = yelp_json_parser.loadFromFile()

	friendshipMap = yelpData[0]
	businessReviews = yelpData[1]
	if buildClean:
			yelpGraph = yelpData[5]
	degreeCentrality = yelpData[2]
	closenessCentrality = yelpData[3]
	betweennessCentrality = yelpData[4]

	print "Betweenness Centralities"
	print len(degreeCentrality)

	# Create appropriate similarity measure (with necessary yelp data) and
	# either calculate similarities from scratch (buildClean == True) or
	# load similarities from file (buildClean == False)
	similarityScores = dict()

	if argv[1] == 'foverlap':
		similarityMeasure = FriendshipOverlapSimilarity(friendshipMap)
	elif argv[1] == 'community':
		similarityMeasure = CommunitySimilarity(yelpGraph)
	elif argv[1] == 'commute':
		similarityMeasure = CommuteTimeSimilarity()
	elif argv[1] == 'pagerank':
		similarityMeasure = PageRankSimilarity(friendshipMap)
	elif argv[1] == 'featureDist':
		factory = FeatureFactory((degreeCentrality, closenessCentrality, betweennessCentrality))
		vectors = factory.getFeatureMatrix()
		similarityMeasure = FeatureDistanceSimilarity(vectors)
	elif argv[1] == 'all':
		similarityMeasure = FriendshipOverlapSimilarity(friendshipMap)
		similarityMeasure.calculateSimilarities()
		similarityScores = similarityMeasure.similarities
		predictionsFOverlap = RegressorUtil.runRegressor(similarityScores, businessReviews, KNNRegressor())

		similarityMeasure = CommunitySimilarity(yelpGraph)
		similarityMeasure.calculateSimilarities()
		similarityScores = similarityMeasure.similarities
		predictionsCommunity = RegressorUtil.runRegressor(similarityScores, businessReviews, KNNRegressor())

		similarityMeasure = PageRankSimilarity(friendshipMap)
		similarityMeasure.calculateSimilarities()
		similarityScores = similarityMeasure.similarities
		predictionsPageRank = RegressorUtil.runRegressor(similarityScores, businessReviews, KNNRegressor())

		factory = FeatureFactory((degreeCentrality, closenessCentrality, betweennessCentrality))
		vectors = factory.getFeatureMatrix()
		similarityMeasure = FeatureDistanceSimilarity(vectors)
		similarityMeasure.calculateSimilarities()
		similarityScores = similarityMeasure.similarities
		predictionsFeatureDist = RegressorUtil.runRegressor(similarityScores, businessReviews, KNNRegressor())

		predictions = RegressorUtil.averagePredictions((predictionsFOverlap,predictionsCommunity,predictionsPageRank,predictionsFeatureDist))
		RegressorUtil.evaluateRegressor(predictions, 'All', 'All')
		sys.exit(0)



	
	if buildClean:
		similarityMeasure.calculateSimilarities()
	else:
		similarityMeasure.loadFromFile()
	
	similarityScores = similarityMeasure.similarities

	print len(similarityScores)

	# Create appropriate prediction model and
	# generate list of predictions
	if argv[2] == 'baseline':
		predictionModel = RandomRegressor(1,5)
	elif argv[2] == 'knn':
		predictionModel = KNNRegressor()

	# Once similarities are calculated, the true ratings are parsed,
	# and the prediction model is chosen, we then run our regression model
	# to generate our predictions for each business-user pair
	predictions = RegressorUtil.runRegressor(similarityScores, businessReviews, predictionModel)

	# Once all the predictions have been calculated, we evaluate the accuracy of
	# our system and report error statistics
	RegressorUtil.evaluateRegressor(predictions, predictionModel.nameLabel, similarityMeasure.nameLabel)


if __name__ == "__main__":
	main(sys.argv)
