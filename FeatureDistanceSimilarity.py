"""
FILE: FeatureDistanceSimilarity.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 12/5/2015
"""

import sys
import json
import networkx as nx
import math
from re import sub
import cPickle as pickle
import yelp_json_parser

class FeatureDistanceSimilarity:

	featureVectors = dict()
	# map of user id -> list of (user id of similar user, similarity score) tuples\
	similarities = dict()
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self, featureVectors, nodeIds):
		self.featureVectors = featureVectors
		self.nameLabel = 'FeatureDistance'

	def loadFromFile(self):
		"""
		Saves calculated similarity score map to file.
		"""
		try:
			f = open( "featureDistSim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	def calculateSimilarities(self):
		for user1 in featureVectors.keys():
			for user2 in featureVectors.keys():
				if user1 == user2: continue
				vec1 = featureVectors[user1]
				vec2 = featureVectors[user2]
				self.similarities[user1] = (user2, cosineDistance(vec1, vec2))

		pickle.dump(self.similarities, open( "featureDistSim.p", "wb" ) )

	def cosineDistance(v1, v2):
		# Normalize vectors
		v1 = norm(v1)
		v2 = norm(v2)
		# Computer Euclidean distance
		distance = 0.0
		for d in xrange(len(v1)):
			distance += math.sqrt(v1[d] - v2[d])

		return distance


	def norm(vec):
		normVec = list()
		for d in xrange(len(vec)):
			normVec.append(vec[d] / sum(vec))
		return normVec







		