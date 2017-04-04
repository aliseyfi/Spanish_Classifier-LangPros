import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

def WikiArticleClassifierTest():
    print("WikiArticleClassifierTest:")
    print("python %s <WikiData>" % sys.argv[0])

if __name__ == '__main__':

    if len(sys.argv) < 6:
        WikiArticleClassifierTest()
        sys.exit(1)

    WikiData = sys.argv[1]
    ArticleClasses = ['Historical', 'Celebrity', 'Geography', 'Academic', 'Business', 'Culture']
    #Need to confirm what categories are being used

    # Read data
    # Need help with integrating data file into this
    trainWikiData = []
    trainWikiLabels = []
    testWikiData = []
    testWikiLabels = []
    
    for current in ArticleClasses:
        WikiDirectory = os.path.join(WikiData, current)
        for fileName in os.listdir(WikiDirectory):
            with open(os.path.join(WikiDirectory, filename), 'r') as f:
                content = f.read()
            #Split data set into training (90% of documents) and testing (10% of documents) using file names
            #If the file starts with "wikiX" for example, then it will run through files X=[1...9]
                if filename.startswith('___'):
                # 10% testing data
                    testWikiData.append(content)
                    testWikiLabels.append(current)
                else:
                # 90% training data
                    trainWikiData.append(content)
                    trainWikiLabels.append(current)

    # Produce feature vectors
    # Included here for my parameters - can remove or change/substitute
    vectorizer = TfidfVectorizer(min_df=6, max_df = 0.75, sublinear_tf=True, use_idf=True)
    trainWikiVectors = vectorizer.fit_transform(trainWikiData)
    testWikiVectors = vectorizer.transform(testWikiData)

    # SVM kernel=rbf Classification
    RBFClassifier = svm.SVC()
    t0 = time.time()
    RBFClassifier.fit(trainWikiVectors, trainWikiLabels)
    t1 = time.time()
    RBFPredictor = RBFClassifier.predict(testWikiVectors)
    t2 = time.time()
    RBFTrainTime = t1-t0
    RBFPredictTime = t2-t1

    # SVM kernel=linear Classification
    LinearClassifier = svm.SVC(kernel='linear')
    t0 = time.time()
    LinearClassifier.fit(trainWikiVectors, trainWikiLabels)
    t1 = time.time()
    LinearPredictor = LinearClassifier.predict(testWikiVectors)
    t2 = time.time()
    LinearTrainTime = t1-t0
    LinearPredictTime = t2-t1

    # SVM kernel=linear Classification
    LibLinearClassifier = svm.LinearSVC()
    t0 = time.time()
    LibLinearClassifier.fit(trainWikiVectors, trainWikiLabels)
    t1 = time.time()
    LibLinearPredictor = LibLinearClassifier.predict(testWikiVectors)
    t2 = time.time()
    LibLinearTrainTime = t1-t0
    LibLinearPredictTime = t2-t1

    # Print results via Table Display
    print("Results for RBF Kernel - Training time: %fs; Prediction time: %fs" % (RBFTrainTime, RBFPredictTime))
    print(classification_report(testWikiLabels, RBFPredictor))
    print("Results for Linear Kernel - Training time: %fs; Prediction time: %fs" % (LinearTrainTime, LinearPredictTime))
    print(classification_report(testWikilabels, LinearPredictor))
    print("Results for Linear SVC - Training time: %fs; Prediction time: %fs" % (LibLinearTrainTime, LibLinearPredictTime))
    print(classification_report(testWikilabels, LibLinearPredictor))
