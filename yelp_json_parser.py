
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
from re import sub
import cPickle as pickle
import matplotlib.pyplot as plt

columnSeparator = "|"
raw_friendship_map = {} # unsanitized friendship map including dead nodes
friendship_map = {} # sanitized friendship map
user_map = {}
review_map = {}
business_map = {}
pair_map = {}
business_reviews = {}

MIN_EDGES = 0

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        print 'Parsing', json_file + '...'
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
        if user not in friendship_map:
            friendship_map[user] = []
        friends = raw_friendship_map[user]
        for friend in friends:
            if friend in raw_friendship_map:
                friendship_map[user].append(friend)

    degree_list = [len(friendship_map[user]) for user in friendship_map]

    degree_counts = [0 for _ in range(0, 1530)]

    for degree in degree_list:
        degree_counts[degree] += 1

    print degree_counts
    plt.loglog(degree_counts, '.')
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    plt.title('PA Degree Distribution')
    plt.show()
    print max(degree_list)


def processReviews():
    print "processReviews()"
    for (user_id, business_id), review in review_map.iteritems():
        if business_id not in business_reviews:
            business_reviews[business_id] = []

        user_rating = review['stars']
        review_entry = (user_id, user_rating)
        business_reviews[business_id].append(review_entry)

    print "Number of businesses reviewed: %d" % len(business_reviews)



# UPDATE by James: now called by RunYelpPredictor, returns values, separate from similarity
def parseJsons(businessJson='pa_business.json', reviewJson='pa_review.json', userJson='pa_user.json'):
    """
    Extracts desired information from the provided Yelp jsons.

    Keyword arguments:
    businessJson -- json storing business relations (default: 'pa_business.json')
    reviewJson   -- json storing ratings of businesses by userJson (default: 'pa_review.json')
    userJson     -- json storing user relations (default: 'pa_user.json')

    Return value:
    a tuple of:
        friendship_map   -- map of user id -> list of user ids of friends
        business_reviews -- map of business id -> list of (user id of user that rated business, rating) tuples
    """

    # loops over all .json files in the argument
    parseJson(businessJson)
    print "Success parsing " + businessJson
    parseJson(reviewJson)
    print "Success parsing " + reviewJson
    parseJson(userJson)
    print "Success parsing " + userJson

    # we won't need the graph for the first part
    # UPDATE by James: initialized because needed to populate friendship_map
    initializeGraph()

