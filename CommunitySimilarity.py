"""
FILE: CommunitySimilarity.py
------------------
TODO: Complete skeleton code
"""

import sys
import json
import networkx as nx
from re import sub
import cPickle as pickle

class CommunitySimilarity:
	"""
	TODO: Figure out how to determine belonging of a user a
	to a community C.
	"""
	# map of user id -> list of (user id of similar user, similarity score) tuples
	similarities = dict()
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self):
		self.nameLabel = 'Community'

	def loadFromFile(self):
		"""
		Saves calculated similarity score map to file.
		"""
		try:
			f = open( "communitySim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	# TODO: Calculate similarity between each pair of nodes
	# 		and store within similarities dict
	def calculateSimilarities(self):
		"""
		TODO: Break up graph into communities, if a user A
		belongs to a community C, similarities[A] = list of (all other nodes in C, score=1) tuples
		"""
		# Calculate similarities and populate similarities dict here


		print "Number of pairs: %d" % len(self.similarities)
		# Write similarity map to file
		pickle.dump(self.similarities, open( "communitySim.p", "wb" ) )