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
corpora = {}
i = 0

for article in data:
    corpora[i] = {}
    words = nltk.word_tokenize(article['text'])
    corpora[i]['words'] = words
    corpora[i]['labels'] = article['category']
    i += 1