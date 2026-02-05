from Data_Storage import Data_Storage
from Final_Prediction_slow import get_final_prediction #Write efficient version later
from Evaluate_Strategy import Evaluate_Strategy


def main():
    ticker = 'ES=F'
    start_date = '2015-01-01'
    end_date = '2020-01-01'
    data_storage = Data_Storage(ticker,start_date , end_date)
    meta_data = data_storage.get_data()
    #meta_direction_list = meta_data['Direction']

    
    

    



    ####### Model Parameters #######

    index_to_start = 300
    index_to_stop =  meta_data.shape[0] - 2 #2??
    lookback = 300

    #This might be alittle dogey
    weight_recent_data= 3 # "weight to recent patterns" # Optimal is around 3 for 300 lookback

    Weight_type_in_lags = 'triangle'  # 'triangle' or 'equal'
    #Weight_type_in_lags = "equal"
    fringe_weight_if_triangle = 0.05  # only used if Weight_type_in_lags == 'triangle'

    #Sometimes some parameters might result in errors.

    ######Trading Logic Parameters######

    #this is asset specific, some are less volatile and have lower return
    expected_return_trade_threshold = 0.001
    predicted_probs_trade_threshold = 0
    transaction_costs = 0.0001
    ################################


    # #1--- Get Predictions for one increment ahead!
    # all_final_predictions, prediction_lags_length = get_final_prediction(data_storage, meta_data, index_to_start, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)

    # #Get Recent lagged pattern and output prediction
    # lagged_pattern_at_head = "".join(map(str, Direction_list[-prediction_lags_length:]))
    # next_increment_prediction = all_final_predictions[lagged_pattern_at_head]
    


    strategy_returns_in_trades_only = []
    all_strategy_returns = []


    #1--- Itterate through timeseries
    for i in range(index_to_start, index_to_stop): 

        current_head_index_of_window = i

        #2---Get predictions
        all_final_predictions, prediction_lags_length, sliced_direction_list  = get_final_prediction(data_storage, meta_data, current_head_index_of_window, lookback, weight_recent_data, Weight_type_in_lags, fringe_weight_if_triangle)
        
        
        lagged_pattern_at_head = "".join(map(str, sliced_direction_list[-prediction_lags_length:]))
        next_increment_prediction = all_final_predictions[lagged_pattern_at_head]

        predicted_return = next_increment_prediction["average_expected_return"]
        predicted_probs = next_increment_prediction["average_probability_of_rising"]

        next_increment_index = current_head_index_of_window + 1
        actual_return = meta_data["Returns"].iloc[next_increment_index]

        print(lagged_pattern_at_head, predicted_return, predicted_probs,actual_return, current_head_index_of_window, "of",index_to_stop )
        




        #3----Trade Logic

        #We buy at the start of the increment and sell at the end, hence out enter exit is just the return at the increment

        #Long
        if predicted_return > expected_return_trade_threshold and predicted_probs > predicted_probs_trade_threshold:
            
            net_long_actual_return = actual_return - transaction_costs
            
            strategy_returns_in_trades_only.append(net_long_actual_return)
            all_strategy_returns.append(net_long_actual_return)
            print("L")
        
        #Short
        elif predicted_return < -expected_return_trade_threshold and predicted_probs < (1 - predicted_probs_trade_threshold):
            
            #We short thus -
            net_short_actual_return = -actual_return - transaction_costs
            strategy_returns_in_trades_only.append(net_short_actual_return)
            all_strategy_returns.append(net_short_actual_return)
            print("S")
        
        #Dont Trade
        else:
            #We dont trade, so returns are 0
            all_strategy_returns.append(0)
    
    Evalaute = Evaluate_Strategy(strategy_returns_in_trades_only, all_strategy_returns)
    Evalaute.get_cumulative_returns_in_trades_only()
    Evalaute.get_cumulative_returns_all_strategy()


    strategy_params = {
    "asset": ticker,
    "date_start_end": [start_date, end_date],
    "index_start_end": [index_to_start,index_to_stop],
    "lookback": lookback,
    "weight_recent": weight_recent_data,
    "weight_type": Weight_type_in_lags,
    "fringe_weight": fringe_weight_if_triangle,
    "ret_threshold": expected_return_trade_threshold,
    "prob_threshold": predicted_probs_trade_threshold,
    "trans_costs": transaction_costs,
    "total_trades": len(strategy_returns_in_trades_only) # Useful extra info
}
    Evalaute.plot_strategy_returns_in_trades_only_with_parameters(strategy_params)

    # print(strategy_returns_in_trades_only)
    # print(all_strategy_returns)
   









    


#Make sure the triangle weights are fine for short pattern lenght/lookback
if __name__ == "__main__":
    print("Hello Leo")
    print("Hello World")
    main()