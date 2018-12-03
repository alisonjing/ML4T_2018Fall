import numpy as np
import pandas as pd
from copy import deepcopy

class RTLearner(object):
    def __init__(self, leaf_size = 1, verbose = False, tree = None):
        self.leaf_size = leaf_size
        self.tree = deepcopy(tree)
    
    def author(self):
        return 'ccheng305'    

    def addEvidence(self, dataX, dataY):
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:,0:dataX.shape[1]] = dataX
        self.model_coefs, self.residuals, self.rank, self.s = np.linalg.lstsq(newdataX, dataY)
        self.tree = self.build_tree(dataX, dataY)
    
    
    def search(self, num, nrow):
            feat, split_val = self.tree[nrow, 0:2]
            if feat == -1: 
                return split_val
            elif num[int(feat)] <= split_val: 
                predict = self.search(num, nrow + int(self.tree[nrow, 2]))
            else: 
                predict = self.search(num, nrow + int(self.tree[nrow, 3]))
            return predict
    
    def query(self, points):
    
        Ytrain = []
        for num in points:
            Ytrain.append(self.search(num, nrow=0))
        return np.asarray(Ytrain)    
        
        
    def build_tree(self, dataX, dataY):
        samples = dataX.shape[0]
        features = dataX.shape[1] 

        leaf = np.array([-1, np.mean(dataY), np.nan, np.nan])
        if (samples <= self.leaf_size): 
            
            return leaf
        
        if (len(pd.unique(dataY)) == 1): 
        
            return leaf 

        
        for p in range(10):
            rand_sample_i = [np.random.randint(0, samples), np.random.randint(0, samples)];
            rand_feature_i = np.random.randint(0, features);
            if dataX[rand_sample_i[1], rand_feature_i] != dataX[rand_sample_i[0], rand_feature_i]:
                break

        if dataX[rand_sample_i[1], rand_feature_i] == dataX[rand_sample_i[0], rand_feature_i]:
            return leaf;

        split_val = (dataX[rand_sample_i[0], rand_feature_i] + dataX[rand_sample_i[1], rand_feature_i]) / 2;
        left_tree = self.build_tree(dataX[(dataX[:, rand_feature_i] <= split_val), :], dataY[(dataX[:, rand_feature_i] <= split_val)]);
        right_tree = self.build_tree(dataX[(dataX[:, rand_feature_i] > split_val), :], dataY[(dataX[:, rand_feature_i] > split_val)]);

        
        if left_tree.ndim > 1:
            root = np.array([rand_feature_i, split_val, 1, left_tree.shape[0] + 1]);
        elif left_tree.ndim == 1:
            root = np.array([rand_feature_i, split_val, 1, 2]);

        
        return np.vstack((root, left_tree, right_tree));




