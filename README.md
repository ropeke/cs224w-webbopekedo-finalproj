# cs224w-webbopekedo-finalproj
A workspace for James Webb, Kelvin Do and Rotimi Opeke to collaborate on their CS224W project. This work should be considered part of the Yelp Academic Challenge and their data should not be utilized unless given prior permission by Yelp!

*~~~~ This should really be a private repository, but we are going to have to settle for now ~~~~~*

# Hey guys!

### Setup:
1. Clone this repository
2. Download and install the networkX package that you can find online here: https://pypi.python.org/pypi/networkx or with pip
3. Download and install numpy module, instructions here: http://docs.scipy.org/doc/numpy/user/install.html


*Goes without saying, but try to use as many comments or add to the README to keep everyone in the loop!*

### Execution:

Quickish-start:
[WARNING: Predicts randomly]   1. python RunYelpPredictor.py foverlap baseline 0 clean
[WARINING: Runtime is an hour] 2. python RunYelpPredictor.py foverlap knn 0

The entire pipeline can be evoked by running the line 'python RunYelpPredictor.py' with the appropriate arguments. The easiest way to get started is to run 'python RunYelpPredictor.py help' or read this README. The following line uses the names of the arguments as placeholders for actual argument values and in the provided order:

python RunYelpPredictor.py -similarityMeasure -predictionModel -trials (-buildClean)

-similarityMeasure

	Description:	A key goal of our project is to experiment and discover the efficacy of different
					similarity measures to help predict business ratings. These similarity measures
					allow us to treat the problem as a k-nearest-neighbors regression problem, where
					our predicted rating for businessB from nodeA is the mean of all ratings of
					businessB done by nodes similar to nodeA.
	
	Accepted Values:

		foverlap		--	Evokes FriendshipSimilarityOverlap. Similarity between nodeA and nodeB is 
							calculated as the ratio of friends A and B have in common / (friends of A + friends of B). This is calculated only on a community level (i.e. for a nodeA will always be at least a friend of a friend of nodeB) in order to reduce runtime.

		mincut			-- 	TODO: implement this similarity measure

		commuteTime		-- 	TODO: implement this similaritu measure (requires pageRank)

		all				-- 	TODO: ~Possibly~ evolve this into a ML problem where all similarity scores 
							are calculated and then weighted using an ML algo

-predictionModel

	Description:	By calculating similarity scores, we have created a de-facto feature space of 1
					dimension, namely the similarity score. Although not the main goal of our project
					we have allowed for experimentation with different regression models to help
					best determine how to interpolate the ratings of similar nodes.

	Accepted Values:

		baseline		--	Evokes RandomRegressor. The rating of a businessB by nodeA is a random
							variable selected uniformly between 1 and 5 (the min and max rating,
							respectively). This serves as a baseline to help better compare the efficacy
							of our experiments.

		knn 			-- 	Evokes KNNRegressor. The rating of a businessB by nodeA is the mean of all
							ratings of businessB done by nodes similar to nodeA. The similarity score
							between nodeA and nodeB is calculated by one of the previously described
							methods. The k-nearest-neighbors to nodeA are determined radially in feature
							space using the hyper-parameter similarityThreshold. This value defines the
							radius for nodeA's neighbors, as no nodes with a similarity score beneath
							the threshold will be counted in the regression.

-trials
	
	Description:	TODO: implement this output feature. The idea is that we can print out the first x
					predictions we made with full details (the business object, the user object, the
					predicted rating, the observed rating, etc).

	Accepetd Values:	

		0 to total number of predictions (integers only)

-buildClean

	Description:	(OPTIONAL) This argument should be ran the first time executing this process. 
					Afterwards, Yelp data will be saved to .bin's that can easily be deserialized in
					code, preventing needless re-parsing of json files. After the first run, this
					argument should be ommitted entirely.

	Accepted Values:

		clean 			--	Evokes yelp_json_parser. All user to user and user to business relationships
							must be re-established and re-parsed by reading from [pa_user, pa_business,
							pa_review].json. Results in the creation of pickle .p files for all 
							subsequent runs.

###Output:
Here is an example output:
~BEGIN EXAMPLE~
###############################
#       ERROR ANALYSIS        #
###############################
Similarity Measure: FriendshipOverlap
Predictor: RandomRegressor
Mean Square Error = 3.42864236072
Error Histogram (prediction - observed):
Error 	Count
-4 		2767
-3 		8106
-2 		12047
-1 		14131
0 		12641
1 		8031
2 		3960
3 		1926
4 		620
Confusion Matrix (predicted rows[1:5], observed cols[1:5]):
	1		2		3		4		5
1	638		750		1231	2593	2767
2	1256	1554	2583	5202	5513
3	1202	1578	2528	5272	5614
4	1156	1529	2594	5166	5526
5	620		770		1229	2603	2755
~END EXAMPLE~

Now in more detail:

Similarity Measure
	
	Description:	Method for measuring the similarity between 2 nodes. Specified with command-line
					argument -similarityMeasure.

Predictor

	Description:	Method for predicting a rating of a business by a node. Specified with command-line
					argument -predictionModel

Mean Square Error

	Description:	An evaluation metric, calculated (1/n)sum_{i=1}^{n}(prediction_i - observed_i)^2. A
					lower MSE implies better prediction.

Error Histogram

	Description:	A more granular breakdown of errors in the model's prediction. Each bin respresents
					a possible difference of (prediction - observed). For instance, the first bin in the example output respresents all instances where prediction = 1, observed = 5.Because predictions are real-numbered, both values are rounded before subtraction to allow for proper indexing.

Confusion Matrix

	Description:	An even more granular breakdown of errors. Each cell (i,j) represents the number of 
					times predicted = i, observed = j. For instance, in the output example, there were 5513 times that predicted = 2, observed = 5. Because predictions are real-numbered, both values are rounded before subtraction to allow for proper indexing.
