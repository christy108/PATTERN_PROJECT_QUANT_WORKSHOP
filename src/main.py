from itertools import count
from Data_Storage import Data_Storage
from Sliding_window import Sliding_window
from Increment import Increment
from pattern_tree.Pattern_tree_map import Pettern_tree_map
import numpy as np
from Weighted_Average import calculate_weighted_averages, weights_to_average

def main():
    data_storage = Data_Storage('TSLA', '2020-01-01', '2023-01-01')
    

    meta_data = data_storage.get_data()

    #print(data)

    lookback = 50
    index_to_start = 100
    weight_recent_data= 20

    slice_data = data_storage.slice_data(meta_data, lookback=lookback, index_to_start=index_to_start)
    print(slice_data)
    print(slice_data["Direction"])
   
    weight_updated_slice = data_storage.update_weights_splitting_on_slice(slice_data, weight_recent_data)

    print(weight_updated_slice)


    #----old code---
    direction_list = weight_updated_slice["Direction"]
    window = Sliding_window(direction_list, 1, 0)
    tree = Pettern_tree_map()
    n = len(direction_list)

    #Sliding Window to get info at head increment
    for length in range(1, n + 1):
        print(f"window length: {length}")
        for i in window.get_start_indices_for_length(length):
            pattern = [str(d) for d in direction_list.iloc[i : i + length]]
            last_index = i + length - 1
            direction = direction_list.iloc[last_index]
            ret = weight_updated_slice["Returns"].iloc[last_index]
            w = weight_updated_slice["weights"].iloc[last_index]
            increment = Increment(direction, ret, w)
            tree.update_leaf_for_increment(pattern, increment)

        leaves_at_depth = tree.count_nodes_at_depth(length)
        if 2**length > leaves_at_depth:
            print(f"  stop: 2^{length}={2**length} > {leaves_at_depth} leaves at depth {length}; pruning depth {length}")
            tree.prune_at_depth(length)
            break


    #---Print Tree---
    tree.compute_derived_stats()
    # tree.print_paths_with_expected_return_bounded(lower=-0.015, upper=0.015)


    #This is the amount of lags we will use to make the prediction, usualy is 6
    prediction_lags_length = length - 2

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