import pandas as pd
import numpy as np
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt

# This class will show a series of trades for the optimal strategy. It is for reference only,
# so it is not used here.
class tos:
    def __init__(self):
        pass
    
    def testPolicy(self, symbol, sd, ed, sv):
        dates = pd.date_range(sd, ed)
        price = get_data(symbol, dates)[symbol]
        
        # Buy or Sell based on price
        df = np.sign(price.diff())
        df = pd.concat([price, df.shift(-1)*1000],axis=1)
        df.columns = ['Price', 'Holdings']
    
        # Compute Trades based on positions held
        df['Trades'] = df['Holdings'].diff()
        df['Trades'].ix[0] = 0
        
        return df['Trades']
    
    
def benchmark(symbol, sd, ed, sv, commission, impact):
    dates = pd.date_range(sd, ed)
    price = get_data(symbol, dates)[symbol]
    bench_mark = pd.DataFrame(np.nan, index = price.index, columns = ['Holdings'])
    bench_mark['Holdings'][0] = 1000
    bench_mark['Holdings'][-1]  = 1000
    bench_mark['Holdings'].ffill(inplace = True)
    bench_mark['Holdings'].fillna(0, inplace = True)
    cost = commission + bench_mark['Holdings'][0] * price.iloc[0,0] * impact
    Cash = sv - bench_mark['Holdings'][0] * price.iloc[0,0] - cost
    port_val = pd.DataFrame(bench_mark.values * price.values + Cash,index = price.index, columns = ['Benchmark'])
    return port_val  
    
def OptimalStrategy(symbol, sd, ed, sv):
    dates = pd.date_range(sd, ed)
    price = get_data(symbol, dates)[symbol]
    
    # Buy or Sell based on price
    result = np.sign(price.diff())
    result = pd.concat([price, result.shift(-1)*1000],axis=1)
    result.columns = ['Price', 'Holdings']
    
    # Compute Trades based on positions held
    result['Trades'] = result['Holdings'].diff()
    result['Trades'].ix[0] = 0
    
    orders_df = result[['Trades']][result['Trades'] != 0]
    price_data = result['Price']
    port_val = compute_portvals(['JPM'], orders_df, price_data, sv, 0, 0)
    
    return result, port_val


def compute_portvals(symbol, orders_df, all_data, start_val, commission=9.95, impact=0.005):
    
    price_date = all_data.index

    holdings = pd.DataFrame(0.0, index=['Position'], columns=symbol)
    holdings['Cash'] = float(start_val)

    port_val = pd.DataFrame(np.zeros((all_data.shape[0], 1)), index=price_date,columns=['Strategy'])

    norm_idx = 0

    for date, order in orders_df.sort_index().iterrows():

        while price_date[norm_idx] < date:

            port_val.iloc[norm_idx, :] = (all_data.loc[price_date[norm_idx]]*holdings.drop('Cash', axis=1)+holdings.loc['Position', 'Cash']).values
            norm_idx += 1

        prices = all_data.loc[date]
        order_detail = np.sign(order.loc['Trades'])
        
        positions = abs(order.loc['Trades'])
        
        cost = commission + prices*impact*positions

        if order_detail == 1:
            holdings['Cash'] -= prices * positions
            holdings['Cash'] -= cost 
            holdings[symbol] += positions
        elif order_detail== -1:
            holdings['Cash'] += prices*positions
            holdings['Cash'] -= cost
            holdings[symbol] -= positions
        else:
            pass
            
    while norm_idx < len(price_date):        
        port_val.iloc[norm_idx, :] = (all_data.loc[price_date[norm_idx]]*holdings.drop('Cash', axis=1) + holdings.loc['Position', 'Cash']).values
        norm_idx += 1

    return port_val


aaa, Optimal = OptimalStrategy(['JPM'], dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 100000)
bench_mark = benchmark(['JPM'], dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 100000, 0, 0)
Bench_vs_Port = pd.concat([bench_mark, Optimal], axis=1)

port_Return = Optimal.iloc[-1] / Optimal.iloc[0] - 1
bench_Return = bench_mark.iloc[-1] / bench_mark.iloc[0] - 1
port_Return_daily = Optimal[1:].values / Optimal[:-1] - 1
bench_Return_daily = bench_mark[1:].values / bench_mark[:-1] - 1

print "The Cumulative Return of the Optimal Strategy is", port_Return[0]
print "The Cumulative Return of the Benchmark is", bench_Return[0]

print "The Average Daily Return of the Optimal Strategy is", port_Return_daily['Strategy'].mean()
print "The Average Daily Return of benchmark is", bench_Return_daily['Benchmark'].mean()

print "The std of the Optimal Strategy is", np.std(port_Return_daily['Strategy'])
print "The std of the benchmark is", np.std(bench_Return_daily['Benchmark'])

    
plt.plot(Optimal/Optimal.iloc[0],color='blue',label='Optimal Strategy')
plt.plot(bench_mark/bench_mark.iloc[0],color='black',label='Benchmark')
plt.title('Optimal Strategy')
plt.ylabel('Portforlio Value')
plt.xlabel('Date')
plt.legend()
plt.show()