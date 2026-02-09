
from Sliding_window import Sliding_window
from Increment import Increment
from pattern_tree.Pattern_tree_map import Pettern_tree_map


#LATER WE CAN PUT THIS IN A CLASS

def populate_tree_predictions(weight_updated_slice):

    "---Populate Pattern Tree--- Get predictions of each pattern"

    direction_list = weight_updated_slice["Direction"]
    window = Sliding_window(direction_list, 1, 0)
    tree = Pettern_tree_map()
    n = len(direction_list)

    #Sliding Window to get info at head increment
    for length in range(1, n + 1):
        #print(f"window length: {length}")
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
            #print(f"  stop: 2^{length}={2**length} > {leaves_at_depth} leaves at depth {length}; pruning depth {length}")
            tree.prune_at_depth(length)
            break
    prediction_lags_length = length - 2
    tree.compute_derived_stats()
    return tree, prediction_lags_length
    # tree.#print_paths_with_expected_return_bounded(lower=-0.015, upper=0.015)


    

def populate_tree_predictions_fast_version(weight_updated_slice):
    # 1. CONVERT TO NUMPY IMMEDIATELY
    # This removes the 17 million 'isinstance' calls
    directions = weight_updated_slice["Direction"].to_numpy()
    returns = weight_updated_slice["Returns"].to_numpy()
    weights = weight_updated_slice["weights"].to_numpy()
    
    window = Sliding_window(directions, 1, 0)
    tree = Pettern_tree_map()
    n = len(directions)

    for length in range(1, n + 1):
        #print(f"window length: {length}")
        
        # Get indices once
        indices = window.get_start_indices_for_length(length)
        
        for i in indices:
            # 2. SLICE NUMPY ARRAYS (NOT PANDAS)
            # Tuple conversion is much faster than [str(d) for d in ...]
            pattern_slice = directions[i : i + length]
            pattern = tuple(pattern_slice) 
            
            last_idx = i + length - 1
            
            # 3. DIRECT ACCESS
            direction = directions[last_idx]
            ret = returns[last_idx]
            w = weights[last_idx]
            
            # Update the tree directly
            # If you can modify 'update_leaf_for_increment' to take 
            # (pattern, direction, ret, w) instead of an object, it will be even faster.
            increment = Increment(direction, ret, w)
            tree.update_leaf_for_increment(pattern, increment)

        leaves_at_depth = tree.count_nodes_at_depth(length)
        if 2**length > leaves_at_depth:
            #print(f"stop: 2^{length} > {leaves_at_depth}; pruning depth {length}")
            tree.prune_at_depth(length)
            break
            
    prediction_lags_length = length - 2
    tree.compute_derived_stats()
    return tree, prediction_lags_length

