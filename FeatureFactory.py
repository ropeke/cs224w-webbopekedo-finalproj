"""
FILE: FeatureFactory.py
------------------
Author: James Webb (jmwebb@stanford.edu)
Created: 12/5/2015
"""

from Prediction import Prediction

class FeatureFactory:
	featureList = list()
	userFeatures = dict()

	def __init__(self, dataset):
		self.featureList = list()
		self.userFeatures = dict()
		self.featureList.append('BetweenessCentrality')
		self.featureList.append('DegreeCentrality')
		self.featureList.append('ClosenessCentrality')

		for userId in dataset[0].keys():
			self.addUser(userId)

		for featureIdx in xrange(len(dataset)):
			featureLabel = self.featureList[featureIdx]
			featureData = dataset[featureIdx]
			for userId in featureData.keys():
				self.addFeature(userId, featureLabel, featureData[userId])


	def addUser(self, userId):
		self.userFeatures[userId] = [0]*len(self.featureList)

	def addFeature(self,userId, featureName, value):
		if featureName in self.featureList:
			self.userFeatures[userId][self.featureList.index(featureName)] = value

	def getFeatureMatrix(self):
		return self.userFeatures