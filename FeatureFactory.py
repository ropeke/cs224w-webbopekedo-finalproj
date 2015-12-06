"""
FILE: FeatureFactory.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 12/5/2015
"""

featureList = list()
userFeatures = dict()

def __init__(self):
	featureList.append('BetweenessCentrality');
	featureList.append('DegreeCentrality');
	featureList.append('ClosenessCentrality');

def addUser(self, userId):
	userFeatures[userId] = [0]*len(featureList)

def addFeature(self, userId, featureName, value):
	if featureName in featureList:
		userFeatures[userId][featureIndexfeatureList().index(featureName)] = value

def getFeatureMatrix(self):
	return userFeatures