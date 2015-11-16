import sys
import json
import networkx as nx
from re import sub
import cPickle as pickle

class FriendshipOverlapSimilarity:

	friendship_map = dict()
	similarities = dict()
	nameLabel = ''



	def __init__(self, friendship_map):
		self.friendship_map = friendship_map
		self.nameLabel = 'FriendshipOverlap'

	def loadFromFile(self):
		try:
			f = open( "foverlapSim.p", "rb" )
			self.similarities = pickle.load(f)
		except IOError as e:
			sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)+'\n')
			sys.stderr.write('Try running with -buildClean = clean!\n')

	"""
	calculateSimilarities - Calculated the similarities between pairs of nodes. We take all pairs of friends of friends to calculate similarities for
	"""
	def calculateSimilarities(self):
		print "calculateSimilarities()"
		# loop through friends
		for user in self.friendship_map:
			if user not in self.similarities:
				self.similarities[user] = list()
			friends = self.friendship_map[user]
			for friend in friends:
				self.similarities[user].append((friend, self.similarityFriendshipOverlap(user, friend)))
				if friend in self.friendship_map:
					# loop through friends of friends
					friend_friends = self.friendship_map[friend]
					for friend_friend in friend_friends:
						self.similarities[user].append((friend_friend, self.similarityFriendshipOverlap(user, friend_friend)))

		print "Number of pairs: %d" % len(self.similarities)
		pickle.dump(self.similarities, open( "foverlapSim.p", "wb" ) )


	"""
	similarityFriendshipOverlap - Finds the similaritiy of two nodes by comparing the 
	fraction of their friends that overlap
	"""
	def similarityFriendshipOverlap(self, node1, node2):
		if node1 not in self.friendship_map or node2 not in self.friendship_map:
			return 0

		friends1 = frozenset(self.friendship_map[node1])
		friends2 = frozenset(self.friendship_map[node2])

		overlap = friends1.intersection(friends2)
		union = friends1.union(friends2)

		return len(overlap) * 1.0 / len(union)