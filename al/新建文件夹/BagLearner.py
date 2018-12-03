import numpy as np
import RTLearner as rt
import LinRegLearner



class BagLearner:
    def __init__(self,learner,kwargs,bags,boost=False,verbose=False):
        self.learner=learner
        self.kwargs=kwargs
        self.bags=bags
        self.learners_list=[]
        for i in range(0,self.bags):
            learner=self.learner(**kwargs)
            self.learners_list.append(learner)
        

    def author(self):
        return 'ccheng305'


    def addEvidence(self,dataX,dataY):
        sample=dataX.shape[0]
        for i in range(0,self.bags):            
            index=np.random.randint(0,sample, size=sample)
            X=dataX[index]
            Y=dataY[index]
            self.learners_list[i].addEvidence(X,Y)

    

    def query(self,Xtest):
        sample=Xtest.shape[0]
        result=self.learners_list[0].query(Xtest)
        for i in range(1,self.bags):
            result+=self.learners_list[i].query(Xtest)
        return result/self.bags
