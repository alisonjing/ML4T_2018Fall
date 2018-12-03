"""Assess a betting strategy.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import matplotlib.pyplot as plt  	  	
		    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def author():  		   	  			    		  		  		    	 		 		   		 		  
        return 'ccheng305' # replace tb34 with your Georgia Tech username.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def gtid():  		   	  			    		  		  		    	 		 		   		 		  
	return 903350007 # replace with your GT ID number  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			    		  		  		    	 		 		   		 		  
	result = False  		   	  			    		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			    		  		  		    	 		 		   		 		  
		result = True  		   	  			    		  		  		    	 		 		   		 		  
	return result  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
	win_prob = 18/38.0 # set appropriately to the probability of a win  		   	  			    		  		  		    	 		 		   		 		  
	np.random.seed(gtid()) # do this only once  		   	  			    		  		  		    	 		 		   		 		  
	print get_spin_result(win_prob) # test the roulette spin  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  

	# add your code here to implement the experiments  		   	  			    		  		  		    	 		 		   		 		  
	   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()

    # Experiment 1
    winnings1 = np.zeros((10,1000))
    winnings1[winnings1 == 0] = 80

    for i in xrange(0, 10):        
        episode_winnings = 0
        counts = 0
        while episode_winnings < 80:
            if counts >= 1000:
                break  
            else:
                won = False
                bet_amount = 1
                while won == False:
                    if counts >= 1000:
                        break
                    won = get_spin_result(18/38.0)
                    if won == True:
                        episode_winnings = episode_winnings + bet_amount
                    else:
                        episode_winnings = episode_winnings - bet_amount
                        bet_amount = bet_amount * 2
                    counts = counts + 1
                    winnings1[i][counts] = episode_winnings
        winnings1[i][0] = 0
    
    Exp1_1_graph = plt.figure(1)
    for ii in xrange(0, 10):
        plt.plot(winnings1[ii])
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('winnings')
    
    winnings2 = np.zeros((1000,1000))
    winnings2[winnings2 == 0] = 80

    # Strategy
    for i in xrange(0, 1000):        
        episode_winnings = 0
        counts = 0
        while episode_winnings < 80:
            if counts >= 1000:
                break  
            else:
                won = False
                bet_amount = 1
                while won == False:
                    if counts >= 1000:
                        break
                    won = get_spin_result(18/38.0)
                    if won == True:
                        episode_winnings = episode_winnings + bet_amount
                    else:
                        episode_winnings = episode_winnings - bet_amount
                        bet_amount = bet_amount * 2
                    counts = counts + 1
                    winnings2[i][counts] = episode_winnings
        winnings2[i][0] = 0
    
    averages = winnings2.mean(0)
    medians = np.median(winnings2, axis = 0)
    stds =  winnings2.std(0)
    average_plus_std = [x + y for x, y in zip(averages, stds)]
    average_minus_std = [x - y for x, y in zip(averages, stds)]
    median_plus_std = [x + y for x, y in zip(medians, stds)]
    median_minus_std = [x - y for x, y in zip(medians, stds)]

    # Draw Graphs
    Exp1_2_graph = plt.figure(2)
    plt.plot(averages, label = 'Mean')
    plt.plot(average_plus_std, label = 'Mean + Std')
    plt.plot(average_minus_std, label = 'Mean - Std')       
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Stats')
    plt.legend()    
    
    Exp1_3_graph = plt.figure(3)  
    plt.plot(medians, label = 'Median')
    plt.plot(median_plus_std, label = 'Median + Std')
    plt.plot(median_minus_std, label = 'Median - Std')  
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Stats')
    plt.legend()        

    # Experiment 2
    winnings3 = np.zeros((1000,1000))
    winnings3[winnings3 == 0] = -256

    # Strategy
    for i in xrange(0, 1000):        
        episode_winnings = 0
        counts = 0
        while episode_winnings > -256 and episode_winnings <= 80:            
            if counts >= 999:
                break  
            else:
                won = False
                bet_amount = 1
                while won == False:
                    if counts >= 999:
                        break
                    else:                        
                        won = get_spin_result(18/38.0)
                        if won == True:
                            episode_winnings = episode_winnings + bet_amount
                        else:
                            episode_winnings = episode_winnings - bet_amount
                            bet_amount = bet_amount * 2
                    
                        money_left = 256 + episode_winnings
                        if money_left < bet_amount:
                            bet_amount = money_left
                        else:
                            pass
                        
                        counts = counts + 1
                        winnings3[i][counts] = episode_winnings
                        
                        if episode_winnings >= 80:
                            winnings3[i][counts+1:] = 80
                            
        winnings3[i][0] = 0

    
    averages3 = winnings3.mean(0)
    medians3 = np.median(winnings3, axis = 0)
    stds3 =  winnings3.std(0)
    average_plus_std3 = [x + y for x, y in zip(averages3, stds3)]
    average_minus_std3 = [x - y for x, y in zip(averages3, stds3)]
    median_plus_std3 = [x + y for x, y in zip(medians3, stds3)]
    median_minus_std3 = [x - y for x, y in zip(medians3, stds3)]    
   
    # Draw graphs
    Exp2_1_graph = plt.figure(4)  
    plt.plot(averages3, label = 'Mean')
    plt.plot(average_plus_std3, label = 'Mean + Std')
    plt.plot(average_minus_std3, label = 'Mean - Std')  
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Stats')
    plt.legend()
    
    Exp2_2_graph = plt.figure(5)  
    plt.plot(medians3, label = 'Median')
    plt.plot(median_plus_std3, label = 'Median + Std')
    plt.plot(median_minus_std3, label = 'Median - Std')  
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Stats')
    plt.legend()

    # Save graphs
    Exp1_1_graph.savefig('Figure 1.png')
    plt.close(Exp1_1_graph)
    Exp1_2_graph.savefig('Figure 2.png')
    plt.close(Exp1_2_graph)
    Exp1_3_graph.savefig('Figure 3.png')
    plt.close(Exp1_3_graph)
    Exp2_1_graph.savefig('Figure 4.png')      
    plt.close(Exp2_1_graph)
    Exp2_2_graph.savefig('Figure 5.png')
    plt.close(Exp2_2_graph)
    
    # Count the probability of wins in 1000 trials
    win_counts = 0
    for i in xrange(0, 1000):
        if winnings3[i][-1] == 80:
            win_counts = win_counts+1
            
    win_counts = win_counts/1000