import pandas as pd
import datetime as dt
from util import get_data, plot_data


def indicator(symbol, sd, ed, back_period):
    
    dates = pd.date_range(sd, ed)
    price = get_data(symbol, dates)[symbol]
    
    rolling_std = price.rolling(window = back_period, min_periods = back_period).std()
    
    # SMA
    SMA = price.rolling(window = back_period, min_periods=back_period).mean()
    
    # Bollinger
    top_band = SMA + (rolling_std * 2)
    bottom_band = SMA - (rolling_std * 2) 
    Bollinger = (price - bottom_band) / (top_band - bottom_band)
            
    # Volatility
    Daily_return = price[1:].values/price[:-1] -1
    temp = price.iloc[-1]
    temp = pd.DataFrame(temp).T
    Daily_return = pd.concat([Daily_return, temp], axis = 0)
    Daily_return = Daily_return.shift(1)
    Daily_return['JPM'][0] = 0.0
    
    VOL = Daily_return.rolling(window = back_period, min_periods = back_period).std()
    
    result = pd.concat([price, SMA, Bollinger, VOL], axis=1)
    result = result.dropna()
    
    result.columns = ['Price', 'SMA', 'Bollinger', 'VOL']
    
    result['Normalized_Price'] = result['Price'] / result['Price'].iloc[0]
    result['Price/SMA'] = result['Price'] / result['SMA']
    result['Normalized_VOL'] = result['VOL'] / result['VOL'].iloc[0]
    
    
    return result




result = indicator(['JPM'], dt.datetime(2008,1,1), dt.datetime(2009,12,31), 14)
    
Bollinger_Plot = result[['Bollinger', 'Normalized_Price']]
plot_data(Bollinger_Plot, title="Bollinger", xlabel="Date", ylabel="Normalized_Price")  

SMA_Plot = result[['Price/SMA', 'Normalized_Price']]
plot_data(SMA_Plot, title="SMA", xlabel="Date", ylabel="Normalized_Price") 

Vol_Plot = result[['Normalized_VOL', 'Normalized_Price']]
plot_data(Vol_Plot, title="Volatility", xlabel="Date", ylabel="Price")


