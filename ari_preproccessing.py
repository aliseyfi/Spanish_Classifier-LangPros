import nltk
import json
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
corpora = {}
i = 0

#todo: this isn't quite working just yet, need to get a word list for feature extraction
for article in data:
    words = nltk.word_tokenize(article['text'])

    corpora[i]['words'] = words
    corpora[i]['labels'] = article['category']
    corpora[i]['title'] = article['title']
    i += 1