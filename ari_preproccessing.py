# Ari Boyarsky (ariboyarsky@gwu.edu)

import nltk
import json
from collections import defaultdict
import itertools
from pprint import pprint

data = []
# currently temp file to speed up debugging
# call data[article #]['type']
# type = [category, text]
with open(r'data\data5.json') as data_file:
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
    # to test within the guidelines of of bluemix we must limit text to 1024 chars
    text = article['text'][:1024]
    text = text.rsplit(' ', 1)[0]
    words = nltk.word_tokenize(text)
    corpora[i]['words'] = words
    corpora[i]['labels'] = article['category']
    i += 1