from Data_Storage import Data_Storage
from Final_Prediction_slow import get_final_prediction #Write efficient version later
from Evaluate_Strategy import Evaluate_Strategy
def main():
    data_storage = Data_Storage('TSLA', '2020-01-01', '2023-01-01')
    meta_data = data_storage.get_data()
    #meta_direction_list = meta_data['Direction']
    

    



    ####### PARAMETERS #######

    index_to_start = 300
    lookback = 300
    weight_recent_data= 10 # "weight to recent patterns"
    Weight_type_in_lags = 'triangle'  # 'triangle' or 'equal'
    #Weight_type_in_lags = "equal"
    fringe_weight_if_triangle = 0.05  # only used if Weight_type_in_lags == 'triangle'

    #Sometimes some parameters might result in errors.

    ###########################



    # #1--- Get Predictions for one increment ahead!
    # all_final_predictions, prediction_lags_length = get_final_prediction(data_storage, meta_data, index_to_start, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)

    # #Get Recent lagged pattern and output prediction
    # lagged_pattern_at_head = "".join(map(str, Direction_list[-prediction_lags_length:]))
    # next_increment_prediction = all_final_predictions[lagged_pattern_at_head]
    


    strategy_returns_in_trades_only = []
    all_strategy_returns = []

    #######Strategy Parameters######
    expected_return_trade_threshold = 0.005
    predicted_probs_trade_threshold = 0.51
    transaction_costs = 0.0001

    ################################

    #1--- Itterate through timeseries
    for i in range(index_to_start, meta_data.shape[0] - 2): #2??

        current_head_index_of_window = i

        #2---Get predictions
        all_final_predictions, prediction_lags_length, sliced_direction_list  = get_final_prediction(data_storage, meta_data, current_head_index_of_window, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)
        
        
        lagged_pattern_at_head = "".join(map(str, sliced_direction_list[-prediction_lags_length:]))
        next_increment_prediction = all_final_predictions[lagged_pattern_at_head]

        predicted_return = next_increment_prediction["average_expected_return"]
        predicted_probs = next_increment_prediction["average_probability_of_rising"]

        next_increment_index = current_head_index_of_window + 1
        actual_return = meta_data["Returns"].iloc[next_increment_index]

        print(lagged_pattern_at_head, predicted_return, predicted_probs,actual_return, current_head_index_of_window, "of",meta_data.shape[0] - 2 )
        




        #3----Trade Logic

        #We buy at the start of the increment and sell at the end, hence out enter exit is just the return at the increment

        #Long
        if predicted_return > expected_return_trade_threshold and predicted_probs > predicted_probs_trade_threshold:
            
            net_long_actual_return = actual_return - transaction_costs
            
            strategy_returns_in_trades_only.append(net_long_actual_return)
            all_strategy_returns.append(net_long_actual_return)
        
        #Short
        elif predicted_return < -expected_return_trade_threshold and predicted_probs < (1 - predicted_probs_trade_threshold):
            
            #We short thus -
            net_short_actual_return = -actual_return - transaction_costs
            strategy_returns_in_trades_only.append(net_short_actual_return)
            all_strategy_returns.append(net_short_actual_return)
        
        #Dont Trade
        else:
            #We dont trade, so returns are 0
            all_strategy_returns.append(0)
    
    Evalaute = Evaluate_Strategy(strategy_returns_in_trades_only, all_strategy_returns)
    Evalaute.get_cumulative_returns_in_trades_only()
    Evalaute.get_cumulative_returns_all_strategy()

    Evalaute.plot_strategy_returns_in_trades_only()

    # print(strategy_returns_in_trades_only)
    # print(all_strategy_returns)
   









    


#Make sure the triangle weights are fine for short pattern lenght/lookback
if __name__ == "__main__":
    print("Hello Leo")
    print("Hello World")
    main()