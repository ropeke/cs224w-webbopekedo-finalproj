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

	def __init__(self, featureVectors):
		self.featureVectors = featureVectors
		for user1 in self.featureVectors.keys():
			self.similarities[user1] = list()
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
		for user1 in self.featureVectors.keys():
			for user2 in self.featureVectors.keys():
				if user1 == user2: continue
				vec1 = self.featureVectors[user1]
				vec2 = self.featureVectors[user2]
				self.similarities[user1].append((user2, self.cosineDistance(vec1, vec2)))

		pickle.dump(self.similarities, open( "featureDistSim.p", "wb" ) )

	def cosineDistance(self, v1, v2):
		# Normalize vectors
		v1 = self.norm(v1)
		v2 = self.norm(v2)
		# Computer Euclidean distance
		distance = 0.0
		for d in xrange(len(v1)):
			distance += math.pow(v1[d] - v2[d], 2)

		distance = math.sqrt(distance)
		return distance


	def norm(self,vec):
		normVec = list()
		if sum(vec) == 0:
			return vec
		for d in xrange(len(vec)):
			normVec.append(vec[d] / sum(vec))
		return normVec







		