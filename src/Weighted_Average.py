
import numpy as np
import matplotlib.pyplot as plt



class weights_to_average:
    "Class that creates weights to average based on lenght of pattern"
    def __init__(self, lenght_of_pattern):
        self.lenght_of_pattern = lenght_of_pattern

    def get_equal_weights(self):
        return [(100/self.lenght_of_pattern/100)] * self.lenght_of_pattern
    
  
    
    def linear_triangle_histogram_weighted(self, fringe_prob):
        "Creates a linear one-peak distribution without dips"
        "Fringe prob is the probability assigned to the first and last slots"
        "Reccommended fringe_prob at 0.04"

        m = self.lenght_of_pattern
        if m == 1:
            return np.array([1.0])
        elif m == 2:
            return np.array([fringe_prob, fringe_prob])
        probs = np.zeros(m)
        probs[0] = probs[-1] = fringe_prob
        n = m - 2
        remaining = 1 - 2 * fringe_prob

        if n % 2 == 1:
            # Odd middle slots → single center
            peak_idx = n // 2
            half_weights = np.arange(1, peak_idx + 2)
            full_weights = np.concatenate([half_weights[:-1], half_weights[::-1]])
        else:
            # Even middle slots → twin centers
            half = n // 2
            half_weights = np.arange(1, half + 1)
            full_weights = np.concatenate([half_weights, half_weights[::-1]])

        # Scale to remaining probability and enforce no dips
        full_probs = full_weights / full_weights.sum() * remaining
        full_probs = np.maximum(full_probs, fringe_prob)
        full_probs *= remaining / full_probs.sum()

        probs[1:-1] = full_probs

        return probs.tolist()
    
    def plot_prob_weights(self, weights):
        "Plots the weights"
        m = self.lenght_of_pattern
        slots = np.arange(1, m + 1)

        plt.figure(figsize=(6, 4))
        plt.bar(slots, weights, color='skyblue')
        plt.xlabel("Slot index")
        plt.ylabel("Probability")
        plt.title(f"Weight Distribution for pattern length={m}")
        plt.xticks(slots)
        plt.ylim(0, max(weights) + 0.05)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.show()


def get_binary_patterns_at_lenght(length):
        "Using lenght, it gets all the binary patterns of that lenght"
        # 1 << length is the same as 2^length
        num_paths = 1 << length
        return [format(i, f'0{length}b') for i in range(num_paths)]



def calculate_weighted_averages(pattern_lenght, tree, weights):
        "Calculates the weighted average expected return and probability of rising for given past patterns.                                                                                                                  "
        "Basically applies the equal or triangle weights to the predictions at different lenghts"
        
       
        final_prediction = {}

        #Get all binary patterns of given lenght
        pattern_list = get_binary_patterns_at_lenght(pattern_lenght)
        
        for pattern in pattern_list:
            
            expected_return_list = []
            probability_of_rising_list = []

            for i in range(len(pattern)):
                sub_pattern = pattern[i:]
                node = tree.get_or_create_leaf_for_path(list(sub_pattern))
                expected_return = node.get_expected_return()
                probability_of_rising = node.get_probability_of_rising()
                
                expected_return_list.append(expected_return if expected_return is not None else 0.0)
                probability_of_rising_list.append(probability_of_rising if probability_of_rising is not None else 0.0)                                                                                                      

            
            weighted_average_expected_return_list = np.array(expected_return_list) * np.array(weights)
            weighted_average_probability_of_rising_list = np.array(probability_of_rising_list) * np.array(weights)
            weighted_average_expected_return = np.sum(weighted_average_expected_return_list)
            weighted_average_probability_of_rising = np.sum(weighted_average_probability_of_rising_list)

            ##print(f"Pattern: {pattern} | Weighted Average Expected Return: {weighted_average_expected_return:.6f} | Weighted Average Probability of Rising: {weighted_average_probability_of_rising:.6f}")

            final_prediction[pattern] = {"average_expected_return": weighted_average_expected_return, "average_probability_of_rising": weighted_average_probability_of_rising}

        return final_prediction