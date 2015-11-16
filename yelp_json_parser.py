
"""
FILE: yelp_json_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modifier: Rotimi Opeke (ropeke@stanford.edu)
Modified: 11/11/2015
"""

import sys
import json
import networkx as nx
from re import sub

columnSeparator = "|"
raw_friendship_map = {} # unsanitized friendship map including dead nodes
friendship_map = {} # sanitized friendship map 
user_map = {}
review_map = {}
business_map = {}
pair_map = {}
business_reviews = {}

#The graph
YGraph = nx.Graph()

MIN_EDGES = 5

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        print "parseJson()"
        num_edges = 0
        for line in f:
            data = json.loads(line)
            if data['type'] == 'user' and len(data['friends']) > MIN_EDGES:
                user_map[data['user_id']] = data
                raw_friendship_map[data['user_id']] = data['friends']
                num_edges += len(data['friends'])
            if data['type'] == 'review':
                review_map[(data['user_id'], data['business_id'])] = data
            if data['type'] == 'business':
                business_map[data['business_id']] = data


def initializeGraph():
    print "initializeGraph()"
    for user in raw_friendship_map:
        YGraph.add_node(user, type="user")
        if user not in friendship_map:
            friendship_map[user] = []
        friends = raw_friendship_map[user] 
        for friend in friends:
            if friend in raw_friendship_map:
                YGraph.add_edge(user, friend)
                friendship_map[user].append(friend)

    print "The number of nodes in the graph is: %d" % YGraph.number_of_nodes()
    print "The number of edges in the graph is: %d" % YGraph.number_of_edges()
    print "Density: %f" % (YGraph.number_of_edges() * 1.0 / YGraph.number_of_nodes())

    print "Finding Communities"
    communities = list(nx.k_clique_communities(YGraph, 7))
    print "Number of communities: %d" % len(communities)
    total_size = 0
    for c in communities:
        print len(c)
        total_size += len(c)
    print "Total size: %d" % total_size


"""
calculateSimilarities - Calculated the similarities between pairs of nodes. We take all pairs of friends of friends to calculate similarities for
"""
def calculateSimilarities():
    print "calculateSimilarities()"
    for user in friendship_map:
        friends = friendship_map[user]
        for friend in friends:
            pair_map[(user, friend)] = similarityFriendshipOverlap(user, friend)
            if friend in friendship_map:
                friend_friends = friendship_map[friend]
                for friend_friend in friend_friends:
                    if (user, friend_friend) not in pair_map:
                        pair_map[(user, friend_friend)] = similarityFriendshipOverlap(user, friend_friend)

    print "Number of pairs: %d" % len(pair_map)


"""
similarityFriendshipOverlap - Finds the similaritiy of two nodes by comparing the 
fraction of their friends that overlap
"""
def similarityFriendshipOverlap(node1, node2):
    if node1 not in friendship_map or node2 not in friendship_map:
        return 0

    friends1 = frozenset(friendship_map[node1])
    friends2 = frozenset(friendship_map[node2])

    overlap = friends1.intersection(friends2)
    union = friends1.union(friends2)

    return len(overlap) * 1.0 / len(union)


def processReviews():
    print "processReviews()"
    for (user_id, business_id), review in review_map.iteritems():
        if business_id not in business_reviews:
            business_reviews[business_id] = []
        
        user_rating = review['stars']
        review_entry = (user_id, user_rating)
        business_reviews[business_id].append(review_entry)

    print "Number of businesses reviewed: %d" % len(business_reviews)


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        parseJson(f)
        print "Success parsing " + f

    # we won't need the graph for the first part
    # initializeGraph()

    # similarities are in the global pair_map
    calculateSimilarities() 

    # business reviews are in the global business_reviews
    processReviews()

    # Continue Coding Here

if __name__ == '__main__':
    main(sys.argv)
