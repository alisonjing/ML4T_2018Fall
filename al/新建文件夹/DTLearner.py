import pandas as pd
import numpy as np
from copy import deepcopy

class DTLearner(object): 
    def __init__(self, leaf_size = 1, verbose = False, tree = None):
        self.leaf_size=leaf_size
        self.tree = deepcopy(tree)
    
    def author(self):
        return 'ccheng305'

    def addEvidence(self, dataX, dataY):
    
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:,0:dataX.shape[1]] = dataX
        self.model_coefs, self.residuals, self.rank, self.s = np.linalg.lstsq(newdataX, dataY)
        ntree = self.build_tree(dataX, dataY)
        if (self.tree == None):
            
            self.tree = ntree
            
        else:
            self.tree = np.vstack((self.tree,ntree))
            
        if (len(self.tree.shape) == 1): 
            self.tree = np.expand_dims(self.tree, axis=0)


    def search(self, num, nrow):
        feat, split_val = self.tree[nrow, 0:2]
        if feat == -1: #Return leaf
            return split_val
        elif num[int(feat)] <= split_val: #Go left is less than split value
            predict = self.search(num, nrow + int(self.tree[nrow, 2]))
        else: #If more, go right
            predict = self.search(num, nrow + int(self.tree[nrow, 3]))
        return predict

    def query(self, points):
        Ytrain = []
        for num in points:
            Ytrain.append(self.search(num, nrow=0))
        return np.asarray(Ytrain)


    def build_tree(self, dataX, dataY):
        samples = dataX.shape[0] #Rows
        leaf = np.array([-1, np.mean(dataY), np.nan, np.nan])
        
        if (samples <= self.leaf_size): 
            return leaf
        
        if (len(pd.unique(dataY)) == 1): 
            return leaf 
        
        if ((np.all(dataY==dataY[0])) | np.all(dataX==dataX[0,:])):
            return leaf
        
        corr = np.abs(np.corrcoef(dataX, y=dataY, rowvar=False))[:-1,-1]
        split_val = np.median(dataX[:,np.nanargmax(corr)])
        smaller_data = dataX[:, np.nanargmax(corr)] <= split_val
        
        if ((np.all(smaller_data)) or np.all(~smaller_data)):
            return leaf
        
        left_tree = self.build_tree(dataX[smaller_data,:], dataY[smaller_data])
        right_tree = self.build_tree(dataX[~smaller_data,:], dataY[~smaller_data])
        
        if left_tree.ndim == 1:
            initial_tree_r = 2
        elif left_tree.ndim > 1:
            initial_tree_r = left_tree.shape[0] + 1
        root = np.array([np.nanargmax(corr), split_val, 1, initial_tree_r])

        return np.vstack((root, left_tree, right_tree))
            

