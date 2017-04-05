# Ari Boyarsky (ariboyarsky@gwu.edu)

from feature_extraction import featureExtractor
import nltk
import json
from collections import defaultdict
import itertools
from pprint import pprint

data = []
# currently temp file to speed up debugging
# call data[article #]['type']
# type = [category, text]
with open(r'data/data5.json') as data_file:
    for line in data_file:
        data.append(json.loads(line))
# pprint(data)

# create word list and labels list for each article
# either feed this to Josh line by line, or create document list of word and label

# corpora object contains a list of words and categories for each article
# call data[article #]['words'] for a list of words
# call data[article #]['labels'] for a list of categories

corpora = {}
i = 0

for article in data:
    corpora[i] = {}
    words = nltk.word_tokenize(article['text'])
    corpora[i]['words'] = words
    corpora[i]['labels'] = article['category']
    i += 1


#########################################
###Josh's Feature Extraction#############
#########################################

myFeatureExtractor = featureExtractor()

#Begin by iterating over the corpora object
for i in corpora:
    document = myFeatureExtractor.createStringObject(corpora[i]['words'])
    myFeatureExtractor.addDocument(document)

#Now train the model
myFeatureExtractor.trainModel()

#print(myFeatureExtractor.model.docvecs.index_to_doctag(0))
#print(myFeatureExtractor.model.most_similar('central'))
#print(myFeatureExtractor.fetchFeatureMatrix())

#Confirm that I can take test data and output a feature vector
#print(myFeatureExtractor.getFeatures(corpora[3]['words']))
