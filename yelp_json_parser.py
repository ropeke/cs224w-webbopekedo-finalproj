
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
friendship_map = {}
user_map = {}
review_map = {}
business_map = {}
pair_map = {}


state_review_list = []
state_business_list = []
state_user_list = []
state_business_set = set()
state_review_map = {}
state_user_map = {}

user_pair_similarity = {}

PRUNE_STATE = 'PA'

# Number k of most similar nodes ot consider
k = 5
#The graph
YGraph = nx.Graph()

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        print "starting to load json file!"
        for line in f:
            data = json.loads(line)
            if data['type'] == 'user':
                user_map[data['user_id']] = data
                friendship_map[data['user_id']] = data['friends']
            if data['type'] == 'review':
                review_map[(data['user_id'], data['business_id'])] = data
            if data['type'] == 'business':
                business_map[data['business_id']] = data

    print len(user_map)


def initializeGraph():
    for user in friendship_map:
        YGraph.add_node(user, type="user")
        friends = friendship_map[user] 
        for friend in friends:
            if friend in friendship_map:
                YGraph.add_edge(user, friend)

    print len(friendship_map)
    print "The number of nodes in the graph is: %d" % YGraph.number_of_nodes()
    print "The number of edges in the graph is: %d" % YGraph.number_of_edges()
    print YGraph.number_of_edges() * 1.0 / YGraph.number_of_nodes()


def calculateSimilarities():
    for user in friendship_map:
        friends = friendship_map[user]
        for friend in friends:
            pair_map[(user, friend)] = similarity_friendship_overlap(user, friend)
            """
            if friend in friendship_map:
                friend_friends = friendship_map[friend]
                for friend_friend in friend_friends:
                    pair_map[(user, friend_friend)] = 2
            """


"""
similarity_friendship_overlap - Finds the similaritiy of two nodes by comparing the 
fraction of their friends that overlap
"""
def similarity_friendship_overlap(node1, node2):
    if node1 not in friendship_map or node2 not in friendship_map:
        return 0

    friends1 = frozenset(friendship_map[node1])
    friends2 = frozenset(friendship_map[node2])

    overlap = friends1.intersection(friends2)
    union = friends1.union(friends2)

    return len(overlap) * 1.0 / len(union)


"""
find_k_most_similar - Finds the k most similar nodes to a given node. Will be extended to support different measures of similarity
"""
def find_k_most_similar(YGraph, node):
    friends = YGraph.neighbors(node)
    sorted_friends = sorted(friends, key=lambda friend: YGraph[node][friend]['friendship_overlap'], reverse=True)
    return sorted_friends[0:k] 


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        parseJson(f)
        print "Success parsing " + f

    # pruneData()
    initializeGraph()
    calculateSimilarities()
    print len(pair_map) * 1.0 / len(friendship_map)
    ##### CONTINUE CODING FROM HERE! ######



if __name__ == '__main__':
    main(sys.argv)
