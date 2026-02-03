from Data_Storage import Data_Storage
from pattern_tree.Populate_Tree_Predictions import populate_tree_predictions
from Weighted_Average import calculate_weighted_averages, weights_to_average
from pattern_tree.Final_Prediction_slow import get_final_prediction

def main():
    data_storage = Data_Storage('TSLA', '2020-01-01', '2023-01-01')
    meta_data = data_storage.get_data()

    ####### PARAMETERS #######

    index_to_start = 500
    lookback = 500
    weight_recent_data= 1 # "weight to recent patterns"
    Weight_type_in_lags = 'triangle'  # 'triangle' or 'equal'
    fringe_weight_if_triangle = 0.09  # only used if Weight_type_in_lags == 'triangle'

    ###########################

    final_prediction = get_final_prediction(data_storage, meta_data, index_to_start, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)
    print(final_prediction)


    



if __name__ == "__main__":
    print("Hello Leo")
    print("Hello World")
    main()