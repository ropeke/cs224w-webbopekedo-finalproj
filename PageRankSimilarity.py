"""
FILE: PageRankSimilarity.py
------------------
TODO: Complete skeleton code
"""

import sys
import json
import networkx as nx
from re import sub
import cPickle as pickle
import random

class PageRankSimilarity:
	"""
	TODO: Figure out how to determine page rank similarity.
	"""
	# map of user id -> list of (user id of similar user, similarity score) tuples
	similarities = dict()
	friendshipMap = {}
	# Useful for debugging/evaluation
	nameLabel = ''
	kNumberRandomWalks = 10000

	def __init__(self, friendshipMap):
		print "INIT PAGERANKSIMILARITY"
		self.nameLabel = 'PageRank'
		self.friendshipMap = friendshipMap

	def loadFromFile(self):
		"""
		Saves calculated similarity score map to file.
		"""
		try:
			f = open( "pageRankSim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	# TODO: Calculate similarity between each pair of nodes
	# 		and store within similarities dict
	def calculateSimilarities(self):
		"""
		TODO: Calculate PageRank between each pair of nodes (prune if too costly).
		"""
		# Calculate similarities and populate similarities dict here
		for user, friends in self.friendshipMap.iteritems():
			# Keep track of number of times a node is randomly visited
			pageRankScores = {}

			# Start user
			currentNode = user
			for i in range(0, self.kNumberRandomWalks):
				# Randomly choose a friend
				friends = self.friendshipMap[currentNode]

				# Continue of friends list is empty
				if not friends:
					continue

				currentNode = random.choice(friends)

				# Add node to tallies
				if currentNode not in pageRankScores:
					pageRankScores[currentNode] = 0

				pageRankScores[currentNode] += 1

			self.similarities[user] = []
			for friend, score in pageRankScores.iteritems():
				self.similarities[user].append((friend, score))


		print "Number of pairs: %d" % len(self.similarities)
		# Write similarity map to file
		pickle.dump(self.similarities, open( "pageRankSim.p", "wb" ) )
