from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing

class featureExtractor:

    def __init__(self):
        #Create empty document list that will be fed into the doc2vec trainer
        self.number = 0
        self.documents = []
        cores = multiprocessing.cpu_count()
        self.model = Doc2Vec(dm=1,dm_mean=1,size=200,window=8,min_count=19,iter=10,workers=cores,alpha=0.025, min_alpha=0.025)  # use fixed learning rate

    def addDocument(self, document):
        self.documents.append(document)

    #Create a sentence object from
    def createStringObject(self, document):
        taggedDoc = TaggedDocument(document, "TRAIN_"+str(self.number))
        self.number = self.number + 1
        return taggedDoc


    #Train the model
    def trainModel(self):
        docIterator = iter(self.documents)

        self.model.build_vocab(docIterator)
        #Helps with accuracy by running over the documents multiple times
        for epoch in range(10):
            self.model.train(docIterator)
            self.model.alpha -= 0.002  # decrease the learning rate
            self.model.min_alpha = self.model.alpha  # fix the learning rate, no decay

        #Remove temp training data
        self.model.delete_temporary_training_data(keep_doctags_vectors=True,keep_inference=True)

        self.model.save("./completedModel.model")


    #Return numpy array of model
    def fetchFeatureMatrix(self):
        train_array = numpy.zeros((self.number,200))

        for i in range(self.number):
            prefix_train = "TRAIN_" + str(i)
            train_array[i] = self.model[prefix_train]

        return train_array

    #Return feature vector for new data
    def getFeatures(self,document):
        return self.model.infer_vector(document)
