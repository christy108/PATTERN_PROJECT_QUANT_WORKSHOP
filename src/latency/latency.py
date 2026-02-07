import yfinance as yf
import pandas as pd

def get_hour_data_for_latency(ticker):

    data = yf.download(ticker, period="2y", interval="1h")
    data.index = pd.to_datetime(data.index)

    return data



ticker = "ES=F"
data = get_hour_data_for_latency(ticker)
#print(data)

returns_list = []
for date, day_df in data.groupby(data.index.date):
    
    #print(f"--- Processing: {date} ---")
    
    # 'day_df' is your "mini df" for this specific day
    # You can now perform any daily logic here


    #print(day_df)
    daily_open = day_df['Open'].iloc[0]
    daily_close = day_df['Close'].iloc[-1]

    returns = (daily_close - daily_open ) / daily_open
    print(returns)
    returns_list.append(returns)
#print(returns_list)



    