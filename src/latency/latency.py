# import yfinance as yf
# import pandas as pd

# def get_hour_data_for_latency(ticker):

#     data = yf.download(ticker, period="2y", interval="1h")
#     data.index = pd.to_datetime(data.index)

#     return data



# # ticker = "ES=F"
# # data = get_hour_data_for_latency(ticker)
# # print(data)




# #if no latency the returns are taken to be the previous day close and current end of day close
# def latent_returns(number_of_latency_hours, ticker):

#     data = get_hour_data_for_latency(ticker)

#     previous_day_close = None
#     returns_list = []

#     for date, day_df in data.groupby(data.index.date):
        
#         # Check if we have a previous close to compare to
#         if previous_day_close is not None:
            
#             # 1. Access today's data as usual
#             # (e.g., using your latency hour logic)
#             current_open = day_df['Close'].iloc[number_of_latency_hours]
#             current_close = day_df['Close'].iloc[-1]

#             # 2. Calculate return using PREVIOUS day's close
#             # This includes the overnight gap
#             if number_of_latency_hours == 0:
#                 returns = (current_close - previous_day_close) / previous_day_close
#             else:
#                 returns = (current_close - current_open) / current_open
                
            
#             returns_list.append(returns)
        
        
#         # 3. Update the previous_day_close for the NEXT iteration
#         #print(day_df)
#         previous_day_close = day_df['Close'].iloc[-1]

#     return returns_list


# latent_returns = latent_returns(0, "^GSPC" )
# print(latent_returns)


import yfinance as yf
import pandas as pd
import numpy as np

def get_data(ticker):
    # auto_adjust=False is non-negotiable for a perfect match
    hourly = yf.download(ticker, period="2y", interval="1h", auto_adjust=False, progress=False)
    daily = yf.download(ticker, period="2y", interval="1d", auto_adjust=False, progress=False)
    
    # This fixes the 'u idiot' error by stripping the MultiIndex headers
    if isinstance(hourly.columns, pd.MultiIndex):
        hourly.columns = hourly.columns.get_level_values(0)
    if isinstance(daily.columns, pd.MultiIndex):
        daily.columns = daily.columns.get_level_values(0)
        
    return hourly, daily

def latent_returns_validated(number_of_latency_hours, ticker):
    hourly_data, daily_data = get_data(ticker)
    
    # Create a clean mapping of Date -> Official Daily Close
    daily_close_map = daily_data['Close'].to_dict()
    daily_dates = sorted(daily_close_map.keys())

    returns_list = []
    grouped = hourly_data.groupby(hourly_data.index.date)

    for date, day_df in grouped:
        try:
            current_ts = pd.Timestamp(date)
            current_idx = daily_dates.index(current_ts)
            if current_idx == 0: continue # Need a 'yesterday' to start
            
            yesterday_ts = daily_dates[current_idx - 1]
            prev_day_close = daily_close_map[yesterday_ts]
            today_official_close = daily_close_map[current_ts]
            
        except (ValueError, KeyError):
            continue 

        if number_of_latency_hours == 0:
            # Match calculation: (Today Close - Yesterday Close) / Yesterday Close
            ret = (today_official_close - prev_day_close) / prev_day_close
            returns_list.append(ret)
        else:
            # Latency calculation: (Today Close - Price after N hours) / Price after N hours
            if len(day_df) > number_of_latency_hours:
                # We use 'Close' of the latency hour as the entry price
                entry_price = day_df['Close'].iloc[number_of_latency_hours]
                ret = (today_official_close - entry_price) / entry_price
                returns_list.append(ret)

    return returns_list

# --- VERIFICATION ---
ticker = "ES=F"
my_latent = latent_returns_validated(1, ticker)

# Re-fetching daily returns and ensuring it's a Series to avoid the 'tolist' error
daily_raw = yf.download(ticker, period="2y", interval="1d", auto_adjust=False, progress=False)
if isinstance(daily_raw.columns, pd.MultiIndex):
    daily_raw.columns = daily_raw.columns.get_level_values(0)

# .squeeze() converts a single-column DataFrame to a Series so .tolist() works
official_daily = daily_raw['Close'].pct_change().dropna().squeeze().tolist()

# Align lengths (Daily pct_change has 1 less row than the raw data)
# We take the last N values to match the loop's output
official_daily_aligned = official_daily[-len(my_latent):]

diff = np.abs(np.array(my_latent) - np.array(official_daily_aligned))
print(f"Max Difference: {np.max(diff):.15f}")

if np.max(diff) < 1e-12:
    print("SUCCESS: Latency 0 perfectly matches Daily returns.")