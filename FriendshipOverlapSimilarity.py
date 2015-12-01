"""
FILE: FriendshipOverlapSimilarity.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 11/15/2015
"""

import sys
import json
import networkx as nx
from re import sub
import cPickle as pickle

class FriendshipOverlapSimilarity:
	"""
	Generates similarity measures between users and their friends of friends
	as according to Yelp Challenge dataset social information. The similarity
	score between a user A and user B is equal to the Jaccard index between the
	set of friends of user A and the set of friends of user B. Note that there
	is not necessariy a similarity score between an arbitrary pair of nodes.
	Because of sparsity, a similarity score exists between user A and user B
	iff user A and user B are friends of friends (if they weren't J(A,B) = 0).
	"""
	# map of user id -> list of user ids of friends
	friendship_map = dict()
	# map of user id -> list of (user id of similar user, similarity score) tuples
	similarities = dict()
	# Useful for debugging/evaluation
	nameLabel = ''

	def __init__(self, friendship_map):
		self.friendship_map = friendship_map
		self.nameLabel = 'FriendshipOverlap'

	def loadFromFile(self):
		"""
		Saves calculated similarity score map to file.
		"""
		try:
			f = open( "foverlapSim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	def calculateSimilarities(self):
		"""
		Calculates the similarities between pairs of nodes. 
		We take all pairs of friends of friends and calculate
		the Jaccard index of their friend sets.
		"""
		# loop through friends
		for user in self.friendship_map:
			if user not in self.similarities:
				self.similarities[user] = list()
			friends = self.friendship_map[user]
			for friend in friends:
				# Find Jaccard index between user and each friend
				self.similarities[user].append((friend, self.similarityFriendshipOverlap(user, friend)))
				if friend in self.friendship_map:
					# loop through friends of friends
					friend_friends = self.friendship_map[friend]
					for friend_friend in friend_friends:
						# Find Jaccard index between user and each friend of friend
						self.similarities[user].append((friend_friend, self.similarityFriendshipOverlap(user, friend_friend)))

		print "Number of pairs: %d" % len(self.similarities)
		# Write similarity map to file
		pickle.dump(self.similarities, open( "foverlapSim.p", "wb" ) )

	def similarityFriendshipOverlap(self, userIdA, userIdB):
		"""
		Finds the similaritiy of two nodes by comparing the 
		fraction of their friends that overlap

		Keyword arguments:
		userIdA -- id of user A, necessary to access friendship map
		userIdB -- id of user B, necessary to access friendship map

		Return value:
		fraction of friends that overlap between user A and user B
		"""
		if userIdA not in self.friendship_map or userIdB not in self.friendship_map:
			return 0

		friends1 = frozenset(self.friendship_map[userIdA])
		friends2 = frozenset(self.friendship_map[userIdB])

		overlap = friends1.intersection(friends2)
		union = friends1.union(friends2)

		return len(overlap) * 1.0 / len(union)