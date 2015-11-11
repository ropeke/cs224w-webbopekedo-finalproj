
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
user_list = list()
# The key here is business_id+user_id
review_list = list()
business_list = list()

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
                user_list.append(data)
            if data['type'] == 'review':
                #print "new review"
                review_list.append(data)
            if data['type'] == 'business':
                #print "new business"
                business_list.append(data)


def initializeGraph():
    YGraph = nx.Graph()
    for user in user_list:
        # print "adding new user node!"
        """
        NOTE:
        ---------------------------------------------------------------------
        Added a "u" before the traditional user_id as they were not unique
        from the business_id's
        """
        YGraph.add_node("u"+user['user_id'], type="user")
    for business in business_list:
        # print "adding new business node!"
        """
        NOTE:
        ---------------------------------------------------------------------
        Added a "b" before the traditional business_id as they were not unique
        from the user_id's
        """
        YGraph.add_node("b"+business['business_id'], type="business")
    # print "The number of nodes in the graph is: %d" % YGraph.number_of_nodes()
    for review in review_list:
        # print "adding a new review"
        user_id = review['user_id']
        business_id = review['business_id']
        YGraph.add_edge("u"+user_id, "b"+business_id, weight=review['stars'])



def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f
    initializeGraph()
    ##### CONTINUE CODING FROM HERE! ######

if __name__ == '__main__':
    main(sys.argv)
