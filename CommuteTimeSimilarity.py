"""
FILE: CommuteTimeSimilarity.py
------------------
TODO: Complete skeleton code
"""

import sys
import json
import networkx as nx
from re import sub
import cPickle as pickle

class CommuteTimeSimilarity:
	"""
	TODO: Figure out how to determine the ECTD between a user A
	and a user B.
	"""
	# map of user id -> list of (user id of similar user, similarity score) tuples
	similarities = dict()
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self):
		self.nameLabel = 'CommuteTime'

	def loadFromFile(self):
		"""
		Saves calculated similarity score map to file.
		"""
		try:
			f = open( "commuteTimeSim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	# TODO: Calculate similarity between each pair of nodes
	# 		and store within similarities dict
	def calculateSimilarities(self):
		"""
		TODO: Calculate ECTD between each pair of nodes (prune if too costly).
		If a user A has an ECTD of X with a user B, sim(A,B) = 1/X.
		similarities[A] = list of (all other user ids, sim score) tuples
		"""
		# Calculate similarities and populate similarities dict here


		print "Number of pairs: %d" % len(self.similarities)
		# Write similarity map to file
		pickle.dump(self.similarities, open( "commuteTimeSim.p", "wb" ) )