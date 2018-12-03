"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			    		  		  		    	 		 		   		 		  

    df=pd.read_csv(orders_file,index_col='Date',parse_dates=True,na_values=['nan'])
    df.sort_index(inplace=True)

    #get the date range
    st=df.index[0]
    et=df.index[-1]
    dates=pd.date_range(st,et)

    #find the symbols in this order file
    listSymbol = []
    for row in df['Symbol']:
        listSymbol.append(row)
    #delete the duplicate ones
    listSymbolUnique = list(set(listSymbol))

    #create the new "Prices" dataframe
    prices = get_data(listSymbolUnique, dates, addSPY=False)
    prices.dropna(inplace=True)
    
    #add one more "cash" column
    prices['cash'] = pd.Series(np.ones(prices.shape[0]), index=prices.index)

    #create the new "Trades" dataframe
    trades=pd.DataFrame(index=prices.index,columns=prices.columns)
    trades.iloc[:]=0

    #go back to work with oders, transform 'buy' and 'sell' to + and -.
    for i in range(df.shape[0]):
        if df.iloc[i,1]=='SELL':
            df.iloc[i,2]=(df.iloc[i,2])*(-1)

    #fill the data of "trades" based on orders
    for i in range(df.shape[0]):
        for j in range(trades.shape[0]):
            if df.iloc[i].name==trades.iloc[j].name:
                trades.iloc[j,-1]=(-df.iloc[i,2])*(prices.iloc[j].loc[df.iloc[i,0]])+trades.iloc[j,-1]-9.95-abs((-df.iloc[i,2])*(prices.iloc[j].loc[df.iloc[i,0]]))*0.005
                trades.iloc[j].loc[df.iloc[i,0]]=trades.iloc[j].loc[df.iloc[i,0]]+df.iloc[i,2]

    #leverage
    leverage=pd.DataFrame(index=prices.index,columns=['leverage'])
    leverage.iloc[0]=1
    for i in range(1,trades.shape[0]):
        if (trades.iloc[i,:]!=0).any()==True:
            temp=((trades.iloc[0:i+1,:]).sum())*(prices.iloc[i,:])
            fenzi=(abs(temp.iloc[0:-1])).sum()
            fenmu=temp.sum()+start_val
            leverage.iloc[i]=fenzi/fenmu
        else:
            leverage.iloc[i]=leverage.iloc[i-1]
    for i in range(1,leverage.shape[0]):
        if leverage.iloc[i,0]>2:
           if leverage.iloc[i,0]>leverage.iloc[i-1,0]:
               trades.iloc[i,:]=0 

    #create the new "Holdings" dataframe
    holdings=pd.DataFrame(index=prices.index,columns=prices.columns)
    holdings.iloc[:]=0
    holdings.iloc[0,-1]=start_val
    holdings.iloc[0]=holdings.iloc[0]+trades.iloc[0]
    
    for i in range(1,holdings.shape[0]):
        holdings.iloc[i]=holdings.iloc[i-1]+trades.iloc[i]
    
    #create the new "Values" dataframe
    #values=pd.DataFrame(index=prices.index,columns=prices.columns)
    values=prices*holdings

    #create the new "port_value" dataframe
    #port_value=pd.DataFrame(index=prices.index,columns=['port_value'])
    port_value=values.sum(axis=1)   


    return port_value  		   	  			    		  		  		    	 		 		   		 		  
    '''
    start_date = dt.datetime(2008,1,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    portvals = get_data(['IBM'], pd.date_range(start_date, end_date))  		   	  			    		  		  		    	 		 		   		 		  
    portvals = portvals[['IBM']]  # remove SPY  		   	  			    		  		  		    	 		 		   		 		  
    rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    return rv  		   	  			    		  		  		    	 		 		   		 		  
    return portvals  		   	  			    		  		  		    	 		 		   		 		  
  		'''
   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    of = "./orders/orders2.csv"  		   	  			    		  		  		    	 		 		   		 		  
    sv = 1000000  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			    		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			    		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			    		  		  		    	 		 		   		 		  
    else:  		   	  			    		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Get portfolio stats  		   	  			    		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		   	  			    		  		  		    	 		 		   		 		  
    print "Date Range: {} to {}".format(start_date, end_date)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of Fund: {}".format(cum_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of Fund: {}".format(std_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Final Portfolio Value: {}".format(portvals[-1])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
