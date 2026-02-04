from pattern_tree.populate_tree_predictions import populate_tree_predictions
from Weighted_Average import calculate_weighted_averages, weights_to_average



def get_final_prediction(data_storage, meta_data, index_to_start, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle):

    #1---Get Data Slice and Update Weights---
    slice_data = data_storage.slice_data(meta_data, lookback=lookback, index_to_start=index_to_start)
    weight_updated_slice = data_storage.update_weights_splitting_on_slice(slice_data, weight_recent_data)
    direction_list = slice_data["Direction"]


    #2---Populate Pattern Tree--- Get predictions of each pattern
    tree, prediction_lags_length = populate_tree_predictions(weight_updated_slice)

    #3---Weights for Weighted Average---
    Weight_object = weights_to_average(prediction_lags_length)

    if Weight_type_in_lags == 'triangle':
        Weight_Probs = Weight_object.linear_triangle_histogram_weighted(fringe_weight_if_triangle)
    elif Weight_type_in_lags == 'equal':
        Weight_Probs = Weight_object.get_equal_weights()
    #Weight_object.plot_prob_weights(Weight_Probs)


    #4---Average Expected Return and Probability of Rising pattern based on weights---
    final_prediction = calculate_weighted_averages(prediction_lags_length, tree, Weight_Probs)
    return final_prediction, prediction_lags_length, direction_list