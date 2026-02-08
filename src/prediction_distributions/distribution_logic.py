import numpy as np


def get_return_percentile(prediction_dict, percentile):
    """
    Calculates the xth percentile of average_expected_return.
    
    Args:
        prediction_dict (dict): The all_final_predictions dict.
        percentile (float): The percentile to compute (0 to 100).
        
    Returns:
        float: The value at the specified percentile.
    """
    # 1. Extract only the returns into a list
    returns = [v['average_expected_return'] for v in prediction_dict.values()]
    
    # 2. Use numpy to find the percentile
    result = np.percentile(returns, percentile)
    
    return result