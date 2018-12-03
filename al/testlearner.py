"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
 		   	  			    		  		  		    	 		 		   		 		    		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import math  		   	  			    		  		  		    	 		 		   		 		  
import DTLearner as dl
import BagLearner as  bl 
import sys  		   	  			    		  		  		    	 		 		   		 		  
import timeit 
import LinRegLearner as lrl
import RTLearner as rl		   	  			    		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
 		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		   	  			    		  		  		    	 		 		   		 		  
        print "Usage: python testlearner.py <filename>"  		   	  			    		  		  		    	 		 		   		 		  
        sys.exit(1)  		   	  			    		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1])  	  			    		  		  		    	 		 		   		 		  
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		   	  			    		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]  		   	  			    		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		    		   	  			    		  		  		    	 		 		   		 		  
    
    # Question 1

    RMSE_insample=[]
    RMSE_outsample=[]
    for i in range(50):
 		   	  			    		  		  		    	 		 		   		 		  
        learner = dl.DTLearner(leaf_size=i) # create a LinRegLearner  		   	  			    		  		  		    	 		 		   		 		  
        learner.addEvidence(trainX, trainY) # train it 
        if i==1: 		   	  			    		  		  		    	 		 		   		 		  
            print learner.author()  		   	  			    		  		  		    	 		 		   		 		  
   	  			    		  		  		    	 		 		   		 		  
        # evaluate in sample  		   	  			    		  		  		    	 		 		   		 		  
        predY = learner.query(trainX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
		   	  			    		  		  		    	 		 		   		 		  
        RMSE_insample.append(rmse)	   	  			    		  		  		    	 		 		   		 		  
      		   	  			    		  		  		    	 		 		   		 		  
        # evaluate out of sample  		   	  			    		  		  		    	 		 		   		 		  
        predY = learner.query(testX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
		   	  			    		  		  		    	 		 		   		 		  
        RMSE_outsample.append(rmse)  		   	  			    		  		  		    	 		 		   		 		  
    curve1,=plt.plot(range(50),RMSE_insample,label='In Sample')
    curve2,=plt.plot(range(50),RMSE_outsample,label='Out of Sample')
    plt.legend(handles=[curve1,curve2])
    plt.savefig('Graph1.png')
    
    #Question 2

    RMSE_insample=[]
    RMSE_outsample=[]
    for i in range(50):
	   	  			    		  		  		    	 		 		   		 		   		   	  			    		  		  		    	 		 		   		 		  
        learner = bl.BagLearner(learner=dl.DTLearner,kwargs={'leaf_size':i},bags=15) 
        
        # Training	   	  			    		  		  		    	 		 		   		 		  
        learner.addEvidence(trainX, trainY) 
         		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
 		   	  			    		  		  		    	 		 		   		 		  
        RMSE_insample.append(rmse)	   	  			    		  		  		    	 		 		   		 		  
      		   	  			    		  		  		    	 		 		   		 		  
        # Out of sample  		   	  			    		  		  		    	 		 		   		 		  
        predY = learner.query(testX) 
        
        # Predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
		   	  			    		  		  		    	 		 		   		 		  
        RMSE_outsample.append(rmse)
  		   	  			    		  		  		    	 		 		   		 		  
    plt.figure()
    curve1,=plt.plot(range(50),RMSE_insample,label='In Sample')
    curve2,=plt.plot(range(50),RMSE_outsample,label='Out of Sample')
    plt.legend(handles=[curve1,curve2])
    plt.savefig('Graph2.png')   
       
    #Question 3
    
    begin = timeit.default_timer()
    for i in range(25):
        learner = dl.DTLearner(leaf_size=15)
        
        # Training DT		   	  			    		  		  		    	 		 		   		 		  
        learner.addEvidence(trainX, trainY)      	   	  			    		  		  		    	 		 		   		 		  
        predY = learner.query(trainX)
    end = timeit.default_timer()
    
    print('Running Time for DT : ', end - begin)
        
    begin = timeit.default_timer()
    for i in range(25):
        learner = rl.RTLearner(leaf_size=15)  		   	  			    		  		  		    	 		 		   		 		  
        learner.addEvidence(trainX, trainY) 
        
        # Training RT        		   	 	    		  		  		    	 		 		   		 		  
        predY = learner.query(trainX)
    end = timeit.default_timer()
    
    print('Running Time for RT: ', end - begin)
    
