import yfinance as yf
import numpy as np

class Data_Storage:
    def __init__(self, ticker, start_date, end_date, split_number_when_equally=1):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

        # Manipulating the data
        self.data["Returns"] = self.data['Close'].pct_change()
        self.data["Direction"] = np.where(self.data["Returns"] > 0, "1", "0")
        self.data["weights"] = self.make_weights_splitting(split_number_when_equally)

    # Utility functions
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data
        return self.data

    # Main functions
    def make_weights_splitting(self, split_number_when_equally):
        "split_number_when_equally: Equally splits the weights"
        "Eg: 2 splits, is a dataset of 10: 5:2s and 5:1s [2,2,2,2,2,1,1,1,1,1]"
        "    3 splits, in a dataset of 12: 4:3s, 4:2s, 4:1s"

        len_data = len(self.data)
        repeats = len_data // split_number_when_equally
        result = []
        for value in range(split_number_when_equally, 0, -1):
            result.extend([value] * repeats)
        amount_to_cut = len_data - len(result)
        if amount_to_cut > 0:
            result.extend([1] * amount_to_cut)
        return result

    def update_weights_splitting(self, split_number_when_equally):
        self.data["weights"] = self.make_weights_splitting(split_number_when_equally)
        return self.data
