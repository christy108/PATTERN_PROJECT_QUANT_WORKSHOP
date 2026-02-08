import matplotlib.pyplot as plt
import seaborn as sns

def plot_from_dict(prediction_dict):
    # 1. Extract values directly using list comprehensions
    returns = [v['average_expected_return'] for v in prediction_dict.values()]
    probs = [v['average_probability_of_rising'] for v in prediction_dict.values()]
    
    # 2. Set the style
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # 3. Plot Returns
    sns.histplot(returns, kde=True, color='teal', bins=10, ax=ax1)
    ax1.set_title('Distribution of Expected Returns', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Expected Return')
    
    # 4. Plot Probabilities
    sns.histplot(probs, kde=True, color='darkorange', bins=10, ax=ax2)
    ax2.set_title('Distribution of Probabilities', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Probability of Rising')
    
    plt.tight_layout()
    plt.show()

