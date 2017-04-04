from feature_extraction import featureExtractor
from feature_reduction import train_pca
import nltk
import numpy
import json
from collections import defaultdict
import itertools
from pprint import pprint
import sys
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report


###################################################
###TUNING PARAMETERS###############################
###################################################
pcaVarianceLevel = 0.5
trainingDataLocation = 'data/data100k.json'
testDataLocation = 'data/data5.json'

###################################################
###Begin by reading in the training data (ARI)#####
###################################################
print('##################### READING IN TRAINING DATA ############################')
trainingData = []
# currently temp file to speed up debugging
# call data[article #]['type']
# type = [category, text]
with open(trainingDataLocation) as data_file:
    for line in data_file:
        trainingData.append(json.loads(line))

# corpora object contains a list of words and categories for each article
# call data[article #]['words'] for a list of words
# call data[article #]['labels'] for a list of categories
trainingCorpora = {}
i = 0

for article in trainingData:
    trainingCorpora[i] = {}
    # to test within the guidelines of of bluemix we must limit text to 1024 chars
    text = article['text'][:1024]
    text = text.rsplit(' ', 1)[0]
    words = nltk.word_tokenize(text)
    trainingCorpora[i]['words'] = words
    trainingCorpora[i]['labels'] = article['category']
    i += 1

###################################################
###Extract Features (JOSH)#########################
###################################################
print('##################### EXTRACTING FEATURES ############################')
trainingLabels = []
myFeatureExtractor = featureExtractor()

#Begin by iterating over the corpora object
for i in trainingCorpora:
    document = myFeatureExtractor.createStringObject(trainingCorpora[i]['words'])
    myFeatureExtractor.addDocument(document)
    trainingLabels.append(trainingCorpora[i]['labels'])

#Now train the model
myFeatureExtractor.trainModel()
trainingFeatures = myFeatureExtractor.fetchFeatureMatrix()

###################################################
###Reduce Features (ELI)###########################
###################################################
print('##################### REDUCING FEATURES ############################')
reducedTrainingFeatures = train_pca(pcaVarianceLevel,trainingFeatures)

###################################################
###Train Classifiers (CHRIS)#######################
###################################################
print('##################### TRAINING CLASSIFIERS ############################')

# SVM kernel=rbf Classification
RBFClassifier = svm.SVC()
#t0 = time.time()
RBFClassifier.fit(reducedTrainingFeatures[1], trainingLabels)
#t1 = time.time()
#t2 = time.time()
#RBFTrainTime = t1-t0
#RBFPredictTime = t2-t1

# SVM kernel=linear Classification
LinearClassifier = svm.SVC(kernel='linear')
#t0 = time.time()
LinearClassifier.fit(reducedTrainingFeatures[1], trainingLabels)
#t1 = time.time()
#t2 = time.time()
#LinearTrainTime = t1-t0
#LinearPredictTime = t2-t1

# SVM kernel=linear Classification
LibLinearClassifier = svm.LinearSVC()
#t0 = time.time()
LibLinearClassifier.fit(reducedTrainingFeatures[1], trainingLabels)
#t1 = time.time()
#t2 = time.time()
#LibLinearTrainTime = t1-t0
#LibLinearPredictTime = t2-t1


######################################################################################################
###FINISHED TRAINING, BEGIN TESTING###################################################################
######################################################################################################


###################################################
###Begin by reading in the test data (ARI)#########
###################################################
print('##################### READING IN TEST DATA ############################')
testData = []
# currently temp file to speed up debugging
# call data[article #]['type']
# type = [category, text]
with open(testDataLocation) as data_file:
    for line in data_file:
        testData.append(json.loads(line))

# corpora object contains a list of words and categories for each article
# call data[article #]['words'] for a list of words
# call data[article #]['labels'] for a list of categories
testCorpora = {}
i = 0
for article in testData:
    testCorpora[i] = {}
    # to test within the guidelines of of bluemix we must limit text to 1024 chars
    text = article['text'][:1024]
    text = text.rsplit(' ', 1)[0]
    words = nltk.word_tokenize(text)
    testCorpora[i]['words'] = words
    testCorpora[i]['labels'] = article['category']
    i += 1

###################################################
###Extract Features (JOSH)#########################
###################################################
print('##################### EXTRACTING TEST FEATURES ############################')
testLabels = []
testFeatures = numpy.zeros((i,500))

#Begin by iterating over the corpora object
for i in testCorpora:
    testFeatures[i] = myFeatureExtractor.getFeatures(testCorpora[i]['words'])
    testLabels.append(testCorpora[i]['labels'])

###################################################
###Reduce Features (ELI)###########################
###################################################
print('##################### REDUCING TEST FEATURES ############################')
reducedTestFeatures = reducedTrainingFeatures[0].transform(testFeatures)

###################################################
###Test Classifiers (CHRIS)########################
###################################################
print('##################### TESTING CLASSIFIERS ############################')
RBFPredictor = RBFClassifier.predict(reducedTestFeatures)
LinearPredictor = LinearClassifier.predict(reducedTestFeatures)
LibLinearPredictor = LibLinearClassifier.predict(reducedTestFeatures)

print("Results for RBF Kernel")
print(classification_report(testLabels, RBFPredictor))
print("Results for Linear Kernel")
print(classification_report(testLabels, LinearPredictor))
print("Results for Linear SVC")
print(classification_report(testLabels, LibLinearPredictor))
