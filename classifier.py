import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

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
