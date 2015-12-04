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
    # TODO
    #    1. Send YGraph value through Json parser
    #    2. get that value as part of CS initializer
    #    3. Use that data to determine community
    #    4. Tuples in same community = 1 | not in same community = 2
	similarities = dict()
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self, yelpGraph):
		self.nameLabel = 'Community'
		self.yelpGraph = yelpGraph

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

		min_community_size = 5

		# Calculate similarities and populate similarities dict here
		print "Finding CommunitySimilarity! Yay!"
		communities = list(nx.k_clique_communities(self.yelpGraph, min_community_size))
		print "Number of test communities: %d" % len(communities)
		total_size = 0
		for c in communities:
			#print len(c)
			total_size += len(c)
		print "Total size: %d" % total_size

		# for each community
		count = 0
		for community in communities:
			print "We've entered a new community!"
			# for every node in the community
			for user in community:
				count += 1
				self.similarities[user] = list()
				# make a list of all other tuples that are in the community (skip self)
				for friend in community:
					if friend != user:
						self.similarities[user].append((friend, 1))
		print "The count is %d" % count


		print "Number of pairs: %d .... should be equal to 2995" % len(self.similarities)
		# Write similarity map to file
		pickle.dump(self.similarities, open( "communitySim.p", "wb" ) )
