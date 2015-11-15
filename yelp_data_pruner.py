
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
user_map = {}
review_map = {}
business_map = {}


state_review_map = {}
state_user_map = {}
state_business_map = {}

PRUNE_STATE = 'NV'

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
        for line in f:
            data = json.loads(line)
            if data['type'] == 'user':
                user_map[data['user_id']] = data
            if data['type'] == 'review':
                review_map[(data['user_id'], data['business_id'])] = data
            if data['type'] == 'business':
                business_map[data['business_id']] = data

    print len(user_map)
    print len(business_map)
    print len(review_map)



def pruneData():
    for (business_id, business) in business_map.iteritems():
        state = business['state']
        if state == PRUNE_STATE:
            state_business_map[business_id] = business

    for (user_id, business_id), review in review_map.iteritems():
        if business_id in state_business_map:
            state_review_map[(user_id, business_id)] = review
            state_user_map[user_id] = user_map[user_id]

    print len(state_business_map)

    with open (PRUNE_STATE + "_business.json", "w") as outfile:
        for business in state_business_map:
            json.dump(state_business_map[business], outfile)
            outfile.write('\n')

    print "finished writing business"

    print len(state_user_map)

    with open (PRUNE_STATE + "_user.json", "w") as outfile:
        for user in state_user_map:
            json.dump(state_user_map[user], outfile)
            outfile.write('\n')

    print "finished writing user"

    print len(state_review_map)
    
    with open (PRUNE_STATE + "_review.json", "w") as outfile:
        for review in state_review_map:
            json.dump(state_review_map[review], outfile)
            outfile.write('\n')

    print "finished writing review"



def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        parseJson(f)
        print "Success parsing " + f

    pruneData()

    print "program complete"

if __name__ == '__main__':
    main(sys.argv)
