# Katherine Walker (kvwalker@gwmail.gwu.edu)

import json
from pprint import pprint
from langdetect import detector
from langdetect import DetectorFactory
from langdetect import language
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException, ErrorCode

f = open('notSpanish.txt', 'w')
with open(r'top1000categories.json') as data_file:
	count = 0;
	for line in data_file:
		pprint(count)
		count = count + 1
		try:
			testing = json.loads(line)
			articleText = testing['text']
			if(detect(articleText) != 'es'): 
				pprint(testing['title'])
				f.write(str((testing['title']).encode('utf-8')))
				f.write("\n")
		except LangDetectException:
			pprint("LangDetectException for article titled " + testing['title'])
f.close()