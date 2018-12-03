"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Chengming Yuan (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: cyuan65 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 903350595 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  	  	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
  
from scipy import optimize		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  
	    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):  
	   	  			    		  		  		    	 		 		   		 		     		  	  		    	 		 		   		 		 		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]   		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  	   

    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)		  			    		  		  		    	 		 		   		 		  
  	   	  			    		  		  		    	 		 		   		 		  	   	  			    		  		  		    	 		 		   		 		  
    allocs = np.ones((1, len(syms))) / len(syms) 
    

    def neg_sharpe_ratio(allocs)	:
        normed = prices / prices.iloc[0,:]
        pos_vals = normed * allocs
        port_val = np.sum(pos_vals, axis=1)
        daily_return = np.diff(port_val) / port_val[0: len(port_val) - 1]        
        adr = sum(daily_return) / len(daily_return)
        sddr = np.std(daily_return)
        sr = adr * np.sqrt(252) / sddr
        neg_sr = -sr
        return neg_sr	  	
    
    # Setting boundary to be 0 - 1, constraints to be 
    constraints = ({ 'type': 'ineq', 'fun': lambda x: np.sum(x) - 1 })
    bounds = [(0.0, 1.0)] * len(syms)
    
    allocs = optimize.minimize(neg_sharpe_ratio, allocs, method='SLSQP', bounds=bounds, constraints=constraints)
    allocs = allocs.x		   	  	
    
    Normed = prices / prices.iloc[0, :]
    
    pos_vals = Normed * allocs
    port_val = pos_vals.sum(axis = 1)
    daily_return = np.diff(port_val) / port_val[0: len(port_val) - 1]
    prices_SPY = prices_SPY / prices_SPY[0]   
    cr = (port_val[-1] - port_val[0]) / port_val[0]
    adr = sum(daily_return) / len(daily_return)
    sddr = np.std(daily_return)
    sr = adr * np.sqrt(252) / sddr		    		
  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		   	  			    		  		  		    	 		 		   		 		  
    if gen_plot:  		   	  			    		  		  		    	 		 		   		 		  
        # add code to plot here  		   	  			    		  		  		    	 		 		   		 		  
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.columns = ['Portfolio', 'SPY']
        plot_data(df_temp, title="Daily Portfolio Value and SPY")  		   	  			    		  		  		    	 		 		   		 		  
        pass  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    return allocs, cr, adr, sddr, sr  		   	  			    		  		  		    	 		 		   		 		  
  


		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2009,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    symbols = ['IBM', 'X', 'GLD', 'JPM']  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", allocations  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio:", sr  		   	  			    		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return:", adr  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return:", cr  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  




