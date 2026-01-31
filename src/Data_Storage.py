import yfinance as yf
import numpy as np

class Data_Storage:
    def __init__(self, ticker, start_date, end_date, split_number_when_equally=1):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        self.split_number_when_equally = split_number_when_equally

        # Put all init logic here!
        self.data["Returns"] = self.data['Close'].pct_change()
        self.data["Direction"] = np.where(self.data["Returns"] > 0, "1", "0")
        self.data["weights"] = self.make_weights_splitting()

    # Utility functions
    def get_split_number_when_equally(self):
        return self.split_number_when_equally
    
    def set_split_number_when_equally(self, split_number):
        self.split_number_when_equally = split_number
        return self.split_number_when_equally
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data
        return self.data

    # Main functions
    def make_weights_splitting(self):
        "split_number_when_equally: Equally splits the weights"
        "Eg: 2 splits, is a dataset of 10: 5:2s and 5:1s [2,2,2,2,2,1,1,1,1,1]"
        "    3 splits, in a dataset of 12: 4:3s, 4:2s, 4:1s"

        len_data = len(self.data)
        split = self.split_number_when_equally
        repeats = len_data // split
        result = []
        for value in range(split, 0, -1):
            result.extend([value] * repeats)
        amount_to_cut = len_data - len(result)
        if amount_to_cut > 0:
            result.extend([1] * amount_to_cut)
        return result