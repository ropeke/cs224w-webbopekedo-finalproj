
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        category = open('category.dat', 'a')
        bids = open('bid.dat', 'a')
        auctions = open('auction.dat', 'a')
        users = open('user.dat', 'a')

        for item in items:
            # for auctions
            auction_table_extract = ""
            item_id = item['ItemID']
            
            seller_id = item['Seller']['UserID']
            seller_id = seller_id.replace('"', '""')
            seller_id = '"'+seller_id+'"'
            
            name = item['Name']
            name = name.replace('"', '""')
            name = '"'+name+'"'
            
            start_time = '"'+transformDttm(item['Started'])+'"'
            end_time = '"'+transformDttm(item['Ends'])+'"'
            
            description = item['Description']
            if (description is None):
                description = 'NULL'
                description = '"'+description+'"'
            if (description != '""'):
                description = description.replace('"','""')
                description = '"'+description+'"'
            current_price = '"'+transformDollar(item['Currently'])+'"'
            first_bid = '"'+transformDollar(item['First_Bid'])+'"'
            num_bids = item.get('Number_of_Bids', "NULL")
            buy_price = item.get('Buy_Price', 'NULL')
            if (buy_price != 'NULL'):
                buy_price = transformDollar(buy_price)
            else:
                buy_price = 'NULL'
            buy_price = '"'+buy_price+'"'

            auction_table_extract += (item_id+columnSeparator+seller_id+columnSeparator+name+columnSeparator+start_time+columnSeparator+end_time+columnSeparator+description+columnSeparator+current_price+columnSeparator+first_bid+columnSeparator+num_bids+columnSeparator+buy_price+"\n")

            # for bids
            bid_length = 0
            if (num_bids != "0"):
                bid_length = len(item['Bids'])

            buying_table_extract = ""
            for i in range(0, bid_length):
                buyer_id = item['Bids'][i]['Bid']['Bidder']['UserID']
                buyer_id = buyer_id.replace('"', '""')
                buyer_id = '"'+buyer_id+'"'
                bid_time = '"'+transformDttm(item['Bids'][i]['Bid']['Time'])+'"'
                bid_amount = '"'+transformDollar(item['Bids'][i]['Bid']['Amount'])+'"'
                buying_table_extract += (item_id+columnSeparator+buyer_id+columnSeparator+bid_time+columnSeparator+bid_amount+"\n")

            # for category
            category_table_extract = ""
            category_length = len(item['Category'])
            for i in range(0, category_length):
                category_entry = item['Category'][i]
                category_entry = '"'+category_entry+'"'
                category_table_extract += (item_id+columnSeparator+category_entry+"\n")

            # for users
            users_table_extract = ""
            seller_rating = item['Seller']['Rating']
            seller_location = item['Location']
            seller_location = '"'+seller_location+'"'
            seller_country = item['Country']
            seller_country = '"'+seller_country+'"'
            users_table_extract += (seller_id+columnSeparator+seller_rating+columnSeparator+seller_location+columnSeparator+seller_country+"\n")

            for i in range(0, bid_length):
                buyer_id = item['Bids'][i]['Bid']['Bidder']['UserID']
                buyer_id = buyer_id.replace('"', '""')
                buyer_id = '"'+buyer_id+'"'
                buyer_rating = item['Bids'][i]['Bid']['Bidder']['Rating']
                buyer_location = item['Bids'][i]['Bid']['Bidder'].get('Location', "NULL")
                buyer_location = '"'+buyer_location+'"'
                buyer_country = item['Bids'][i]['Bid']['Bidder'].get('Country', "NULL")
                buyer_country = '"'+buyer_country+'"'
                users_table_extract += (buyer_id+columnSeparator+buyer_rating+columnSeparator+buyer_location+columnSeparator+buyer_country+"\n")


            bids.write(buying_table_extract)
            category.write(category_table_extract)
            auctions.write(auction_table_extract)
            users.write(users_table_extract)
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
