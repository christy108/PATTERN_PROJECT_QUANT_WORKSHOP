import yfinance as yf
import numpy as np

class Data_Storage:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

        # Manipulating the data
        self.data["Returns"] = self.data['Close'].pct_change()
        self.data["Direction"] = np.where(self.data["Returns"] > 0, "1", "0")
        self.data["weights"] = [1] * len(self.data)

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
