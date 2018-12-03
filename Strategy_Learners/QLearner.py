"""  		   	  			    		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import random as rand  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class QLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna
        self.q = np.random.uniform(-1.0, 1.0, size=(num_states, num_actions))

        self.s = []
        self.a = []
        self.Stored = []
  		   	  			    		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		   	  			    		  		  		    	 		 		   		 		  
        	  		    	 		 		   		 		  
        self.s = s
        option = rand.random()

        if option >= self.rar:
            action = np.argmax(self.q[self.s])
        else:
            action = rand.randint(0, self.num_actions - 1)
    

        if self.verbose:
            print "s =", s, "a =", action
        else:
            pass
        
        return action
  		   	  			    		  		  		    	 		 		   		 		  
    def query(self, s_prime, r):  		   	  			    		  		  		    	 		 		   		 		  
        
        option = rand.random()
        temp = self.alpha*(r+self.q[s_prime, np.argmax(self.q[s_prime])]*self.gamma)+self.q[self.s, self.a]*(1.0-self.alpha)
        self.q[self.s, self.a] = temp
        self.Stored.append([self.s, self.a, s_prime, r])        
        
        if option >= self.rar:            
            action = np.argmax(self.q[s_prime])           
        else:            
            action = rand.randint(0, self.num_actions - 1) 

       
        if self.dyna == 0:
            pass
        else:
            index = np.random.choice(len(self.Stored), size = self.dyna, replace = True)
            for i in index:
                dyna_state, dyna_action, state_p, rr = self.Stored[i]
                temp = self.q[dyna_state, dyna_action]*(1.0-self.alpha)+(rr+self.gamma*self.q[state_p, np.argmax(self.q[state_p])])*self.alpha
                self.q[dyna_state, dyna_action] = temp
        
        if self.verbose: 
            print "s =", s_prime, "a =", action, "r =", r
        else:
            pass

        self.a = action
        self.s = s_prime
        self.rar = self.radr * self.rar

        return action

    def author(self):
        return 'ccheng305'
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "Remember Q from Star Trek? Well, this isn't him"  		   	  			    		  		  		    	 		 		   		 		  

