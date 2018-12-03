import pandas as pd
import numpy as np
import datetime as dt
from util import get_data
from indicators import indicator
from TheoreticallyOptimalStrategy import compute_portvals, benchmark
import matplotlib.pyplot as plt

# This class will produces a series of trades. It is for reference only, so it is not used
class ms:
    def __init__(self):
        pass
    
    def testPolicy(self, symbol, sd, ed, sv):
        result = indicator(list(set(symbol)), sd, ed, back_period=14)
        SMA = result[['Price/SMA']]
    
        SMA_records = pd.DataFrame(0, index=SMA.index,columns=SMA.columns)
        SMA_records[SMA >= 1] = 1
        SMA_records[1:] = SMA_records.diff()
        SMA_records.ix[0] = 0
        SMA_records = SMA_records.rename(columns={'Price/SMA': 'SMA_records'})
        result = pd.concat([result, SMA_records], axis=1)
    
        
        result[['Holdings']] = pd.DataFrame(np.nan, index=result.index, columns=['Holdings'])
        # Buy/Sell conditions 
        result['Holdings'][(result['Normalized_VOL'] < 0.2)] = 1000
        result['Holdings'][(result['Bollinger'] > 0.8)] = -1000
        result['Holdings'][(result['SMA_records'] != 0)] = 0
        
        result['Holdings'].ffill(inplace = True)
        result['Holdings'].fillna(0, inplace=True)
        result['Trades'] = result['Holdings'].diff()
        result['Trades'].ix[0] = 0
        df_trades = result['Trades']
        return df_trades 


def ManualStrategy(symbol, sd, ed, sv):
    result = indicator(list(set(symbol)), sd, ed, back_period=14)
    SMA = result[['Price/SMA']]
    
    # Prepare for the buy and sell graph
    SMA_records = pd.DataFrame(0, index=SMA.index,columns=SMA.columns)
    SMA_records[SMA >= 1] = 1
    SMA_records[1:] = SMA_records.diff()
    SMA_records.ix[0] = 0
    SMA_records = SMA_records.rename(columns={'Price/SMA': 'SMA_records'})
    result = pd.concat([result, SMA_records], axis=1)
    
    
    result[['Holdings']] = pd.DataFrame(np.nan, index=result.index, columns=['Holdings'])
    
    # Buy/Sell conditions
    result['Holdings'][(result['Normalized_VOL'] < 0.2)] = 1000
    result['Holdings'][(result['Bollinger'] > 0.8)] = -1000
    result['Holdings'][(result['SMA_records'] != 0)] = 0
    result['Holdings'].ffill(inplace=True)
    result['Holdings'].fillna(0, inplace=True)
    result['Trades'] = result['Holdings'].diff()
    result['Trades'].ix[0] = 0
    orders_df = result[['Trades']][result['Trades']!=0]
    price_data = result['Price']
    port_val = compute_portvals(['JPM'], orders_df, price_data, start_val=sv, commission=9.95, impact=0.005)
    return result,port_val


result, Manual = ManualStrategy(['JPM'], dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), 100000)
bench_val = benchmark(['JPM'], dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), 100000, 9.95, 0.005)
Bench_vs_Port = pd.concat([bench_val, Manual], axis=1)


port_Return = Manual.iloc[-1]/Manual.iloc[0] - 1
bench_Return = bench_val.iloc[-1]/bench_val.iloc[0] - 1
manual_daily_return = Manual.diff()/ Manual[0:len(Manual)].shift(1)
daily_return_bench = bench_val.diff() / bench_val[0:len(bench_val)].shift(1)

print 'The cumulative return of the strategy is', port_Return[0]
print 'The cumulative return of benchmark is', bench_Return[0]

print 'The average daily return of the strategy is', manual_daily_return['Strategy'].dropna().mean()
print 'The standard deviation of daily return of the strategy is', np.std(manual_daily_return['Strategy'].dropna())

print 'The average daily return of benchmark is', daily_return_bench['Benchmark'].dropna().mean()
print 'The standard deviation of daily return of benchmark is', np.std(daily_return_bench['Benchmark'].dropna())



plt.plot(Manual/Manual.iloc[0],color='blue',label='Manual Strategy')
plt.plot(bench_val/bench_val.iloc[0],color='black',label='Benchmark')
plt.title('Manual Strategy')
plt.ylabel('Value')
plt.xlabel('Date')
plt.legend()


for index, marks in result.iterrows():
    if marks['Trades'] == 1000:
        plt.axvline(x=index, color='green',linestyle='dashed')
    elif marks['Trades'] == -1000:
        plt.axvline(x=index, color='red',linestyle='dashed')
    else:
        pass
    
plt.show()




