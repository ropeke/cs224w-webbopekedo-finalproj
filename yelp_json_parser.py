
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
user_edges = {}
# The key here is business_id+user_id
review_list = list()
business_list = list()
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
                #print "new user!"
                user_edges[data['user_id']] = data['friends']
            if data['type'] == 'review':
                #print "new review"
                review_list.append(data)
            if data['type'] == 'business':
                #print "new business"
                business_list.append(data)


def initializeGraph():
    for user in user_edges:
        """
        NOTE:
        ---------------------------------------------------------------------
        Added a "u" before the traditional user_id as they were not unique
        from the business_id's
        """
        user_id = "u" + user
        YGraph.add_node(user_id, type="user")
        
        for friend in user_edges[user]:
            friend_id = "u" + friend
            if friend in user_edges:
                friendship_overlap = similarity_friendship_overlap(user, friend)
            else:
                friendship_overlap = 0
            YGraph.add_edge(user_id, friend_id, friendship_overlap=friendship_overlap)


    for business in business_list:
        # print "adding new business node!"
        """
        NOTE:
        ---------------------------------------------------------------------
        Added a "b" before the traditional business_id as they were not unique
        from the user_id's
        """
        YGraph.add_node("b"+business['business_id'], type="business")


    for review in review_list:
        # print "adding a new review"
        user_id = review['user_id']
        business_id = review['business_id']
        YGraph.add_edge("u"+user_id, "b"+business_id, weight=review['stars'])

    print "The number of nodes in the graph is: %d" % YGraph.number_of_nodes()
    print "The number of edges in the graph is: %d" % YGraph.number_of_edges()


"""
similarity_friendship_overlap - Finds the similaritiy of two nodes by comparing the 
fraction of their friends that overlap
"""
def similarity_friendship_overlap(node1, node2):
    friends1 = frozenset(user_edges[node1])
    friends2 = frozenset(user_edges[node2])

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
    initializeGraph()
    ##### CONTINUE CODING FROM HERE! ######
    for node in YGraph.nodes():
        print find_k_most_similar(YGraph, node)



if __name__ == '__main__':
    main(sys.argv)
