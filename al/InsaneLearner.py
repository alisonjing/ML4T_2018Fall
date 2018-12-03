import numpy as np
import LinRegLearner as ll
import BagLearner as bl

class InsaneLearner:
    def __init__(self,verbose=False):
        self.learner=bl.BagLearner(learner = bl.BagLearner,
                                   kwargs = {"learner":ll.LinRegLearner, "kwargs":{"verbose":False},"bags":20, "boost":False, "verbose":False},
                                   bags = 20, boost = False, verbose = False)
    
    def author(self):
        return 'ccheng305'        

    def addEvidence(self,dataX,dataY):
        self.learner.addEvidence(dataX,dataY)



    def query(self,Xtest):
        return self.learner.query(Xtest)
