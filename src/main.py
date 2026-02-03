from Data_Storage import Data_Storage
from Final_Prediction_slow import get_final_prediction #Write efficient version later

def main():
    data_storage = Data_Storage('TSLA', '2020-01-01', '2023-01-01')
    meta_data = data_storage.get_data()
    Direction_list = meta_data['Direction']
    

    



    ####### PARAMETERS #######

    index_to_start = 600
    lookback = 600
    weight_recent_data= 1 # "weight to recent patterns"
    Weight_type_in_lags = 'triangle'  # 'triangle' or 'equal'
    fringe_weight_if_triangle = 0.05  # only used if Weight_type_in_lags == 'triangle'

    #Sometimes some parameters might result in errors.

    ###########################



    #1--- Get Predictions for one increment ahead!
    all_final_predictions, prediction_lags_length = get_final_prediction(data_storage, meta_data, index_to_start, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)

    #Get Recent lagged pattern and output prediction
    lagged_pattern_at_head = "".join(map(str, Direction_list[-prediction_lags_length:]))
    next_increment_prediction = all_final_predictions[lagged_pattern_at_head]
    


    #2--- Simulate the Trading

    for i in range(index_to_start + 1 , meta_data.shape[0] - 2): #2??

        current_head_index_of_window = i

        #---Get predictions
        all_final_predictions, prediction_lags_length  = get_final_prediction(data_storage, meta_data, current_head_index_of_window, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)
        
        
        ####### WE ALSO HAVE TO UPDATE THE DIRECTION LIST write a fucntion splitting the data??


        lagged_pattern_at_head = "".join(map(str, Direction_list[-prediction_lags_length:]))
        next_increment_prediction = all_final_predictions[lagged_pattern_at_head]

        predicted_return = next_increment_prediction["average_expected_return"]
        predicted_probs = next_increment_prediction["average_probability_of_rising"]

        print(lagged_pattern_at_head, predicted_return, predicted_probs, current_head_index_of_window )
        


    #print(lagged_pattern,next_increment_prediction, meta_data["Returns"].iloc[index_to_start])


    



if __name__ == "__main__":
    print("Hello Leo")
    print("Hello World")
    main()