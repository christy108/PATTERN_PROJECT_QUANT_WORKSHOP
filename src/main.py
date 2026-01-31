from Data_Storage import Data_Storage
from Sliding_window import Sliding_window
from Increment import Increment
from pattern_tree.Pattern_tree_map import Pettern_tree_map

def main():
    data_storage = Data_Storage('AAPL', '2020-01-01', '2023-01-01', 5)
    data = data_storage.get_data()
    direction_list = data["Direction"]

    window = Sliding_window(direction_list, 1, 0)
    tree = Pettern_tree_map()
    n = len(direction_list)

    for length in range(1, n + 1):
        print(f"window length: {length}")
        for i in window.get_start_indices_for_length(length):
            pattern = [str(d) for d in direction_list.iloc[i : i + length]]
            last_index = i + length - 1
            direction = direction_list.iloc[last_index]
            ret = data["Returns"].iloc[last_index]
            w = data["weights"].iloc[last_index]
            increment = Increment(direction, ret, w)
            tree.update_leaf_for_increment(pattern, increment)

        leaves_at_depth = tree.count_nodes_at_depth(length)
        if 2**length > leaves_at_depth:
            print(f"  stop: 2^{length}={2**length} > {leaves_at_depth} leaves at depth {length}; pruning depth {length}")
            tree.prune_at_depth(length)
            break

    tree.print_tree()

    tree.print_paths_with_expected_return_bounded(lower=-0.005, upper=0.005)


if __name__ == "__main__":
    main()