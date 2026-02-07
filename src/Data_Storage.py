import yfinance as yf
import numpy as np
from latency.latency import apply_latency_hours_returns, get_hourly_data_latency   

class Data_Storage:
    def __init__(self, ticker, num_years, apply_latency, if_latency_how_much):
        self.ticker = ticker
        self.num_years = num_years
        self.data = yf.download(ticker, period=f"{num_years}y", interval="1d", auto_adjust=False, progress=False)

        # Manipulating the data

        if apply_latency == False:
            self.data["Returns"] = self.data['Close'].pct_change()

        

    # Utility functions
    def get_data(self):
        "Get data, hourly if latent"
        if self.latency == True:
            latency_data = get_hourly_data_latency(self.ticker)
            latent_returns = apply_latency_hours_returns(latency_data, self.if_latency_how_much)
            self.data["Returns"] = latent_returns
        self.data["Direction"] = np.where(self.data["Returns"] > 0, "1", "0")
        self.data["weights"] = [1] * len(self.data)
        return self.data
    
    def slice_data(self, data, lookback, index_to_start):
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
