from Data_Storage import Data_Storage
from pattern_tree.Populate_Tree import populate_tree
from Weighted_Average import calculate_weighted_averages, weights_to_average

def main():
    data_storage = Data_Storage('TSLA', '2020-01-01', '2023-01-01')
    

    meta_data = data_storage.get_data()


    lookback = 100
    index_to_start = 100
    weight_recent_data= 20
    
    slice_data = data_storage.slice_data(meta_data, lookback=lookback, index_to_start=index_to_start)
    weight_updated_slice = data_storage.update_weights_splitting_on_slice(slice_data, weight_recent_data)

    

    #---Populate Pattern Tree--- Get predictions of each pattern
    tree, prediction_lags_length = populate_tree(weight_updated_slice)

    #---Weights for Weighted Average---
    Weight_object = weights_to_average(prediction_lags_length)
    Weight_Probs_triangle = Weight_object.linear_triangle_histogram_weighted(0.09)
    Weight_probs_equal = Weight_object.get_equal_weights()
    #Weight_object.plot_prob_weights(Weight_Probs)
    
    #---Average Expected Return and Probability of Rising pattern---
    final_prediction = calculate_weighted_averages(prediction_lags_length, tree, Weight_probs_equal)
    print(final_prediction)



    



if __name__ == "__main__":
    print("Hello Leo")
    print("Hello World")
    main()