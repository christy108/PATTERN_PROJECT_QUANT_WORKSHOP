import yfinance as yf
import numpy as np
import pandas as pd
class Data_Storage:
    def __init__(self, ticker, start_date, end_date, latency = True):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

         # Manipulating the data
        self.data["Returns"] = self.data['Close'].pct_change()
        self.data["Direction"] = np.where(self.data["Returns"] > 0, "1", "0")
        self.data["weights"] = [1] * len(self.data)

        #Observing the returns if we didnt have latency
        if latency == False:
            print("Make sure start date is two years prior from today")
            self.data["non_latent_returns"]  = self.merge_download_non_latent_returns()

       
    # Utility functions
    def get_data(self):
        return self.data
    
    def slice_data(self,data, lookback, index_to_start):
        window_error = index_to_start - lookback 
        if window_error < 0:
            print()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"Warning: window error: {window_error} < 0")
            print(f"Increase index or decrease lookback by: {abs(window_error)}")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print()
        else:   

            head_index = index_to_start 
            tail_index = index_to_start - lookback 
            data = data.iloc[tail_index:head_index]
            print(f"Data sliced from index {tail_index} to {head_index}")
            return data

    # Main functions
    def update_weights_splitting_on_slice(self, slice_data, split_number_when_equally):
        slice_data["weights"] = self.make_weights_splitting(slice_data, split_number_when_equally)
        return slice_data
    
    def make_weights_splitting(self, slice_data,  split_number_when_equally):
        "split_number_when_equally: Equally splits the weights"
        "Eg: 2 splits, is a dataset of 10: 5:2s and 5:1s [2,2,2,2,2,1,1,1,1,1]"
        "    3 splits, in a dataset of 12: 4:3s, 4:2s, 4:1s"

        len_data = len(slice_data)
        repeats = len_data // split_number_when_equally
        result = []
        for value in range(split_number_when_equally, 0, -1):
            result.extend([value] * repeats)
        amount_to_cut = len_data - len(result)
        if amount_to_cut > 0:
            result.extend([1] * amount_to_cut)
        return result
    

    def download_non_latent_returns(self, latent_hours=1):

        "Downloads 2y of hourly data, calculates the return of non latent closes"
        "The actual price we buy and sell at is the end of day closes"
        "The returns we are calucalting is where we ask the market to buy or sell, aka one, two, three hours before the end of the day"
        "These returns assume no latency"

        hourly_data = yf.download(self.ticker, period="2y", interval="1h", auto_adjust=False, progress=False)

        # If the ticker is in the columns (MultiIndex), flatten it immediately
        if isinstance(hourly_data.columns, pd.MultiIndex):
            hourly_data = hourly_data.droplevel(1, axis=1) # Drop the Ticker level

        #group each day in the hourly data to then itterate.
        grouped = hourly_data.groupby(hourly_data.index.date)

        non_latency = latent_hours + 1
        dict_list = []
        for date, day_df in grouped:
            dict_list.append({
                "Date": date,
                "non_latent_close": day_df["Close"].iloc[-non_latency]
            })
        new_df = pd.DataFrame(dict_list)
        new_df["non_latent_returns"] = new_df["non_latent_close"].pct_change()

        return new_df
    

    def merge_download_non_latent_returns(self):

        "Merge the latent returns with non latent returns for as much data as we have"
        non_latent_df = self.download_non_latent_returns()

        first_day_non_latent_returns = non_latent_df["Date"].iloc[0]

        updated_non_latency = self.data['Returns'].copy()
        updated_non_latency.name = 'non_latent_returns'
        
        # We set 'Date' as index and filter for dates AFTER the cutoff
        updates = non_latent_df.set_index('Date')
        updates = updates.loc[updates.index > first_day_non_latent_returns, 'non_latent_returns']
        
        # 3. Apply the update
        # Because both are now indexed by Date, Pandas aligns them perfectly
        updated_non_latency.update(updates)
        
        self.data['non_latent_returns'] = updated_non_latency

        # print(non_latent_df)

        # print(self.data)


        # #self.data.to_csv("Debug.csv")
        
        return updated_non_latency