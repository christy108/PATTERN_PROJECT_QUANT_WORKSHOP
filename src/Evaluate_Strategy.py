import pandas as pd
import matplotlib.pyplot as plt

class Evaluate_Strategy:

    
    #Can add date too for plotting
    def __init__(self, strategy_returns_in_trades_only, all_strategy_returns):
        self.strategy_returns_in_trades_only = pd.Series(strategy_returns_in_trades_only)
        self.all_strategy_returns = pd.Series(all_strategy_returns)
        
    

    def get_cumulative_returns_in_trades_only(self):
        cum_ret = (1 + self.strategy_returns_in_trades_only).cumprod() - 1

        return cum_ret*100

    
    def get_cumulative_returns_all_strategy(self):
        cum_ret = (1 + self.all_strategy_returns).cumprod() - 1
        return cum_ret*100



    def plot_strategy_returns_in_trades_only(self, title="Cumulative Strategy Returns per Trade)"):
        """
        Plots the cumulative returns of a strategy focusing only on periods within trades.
        
        Parameters:
        returns_series (pd.Series): Series of returns.
        title (str): Title of the plot.
        """
        # Calculate cumulative returns
        # Assuming the returns are simple returns. 
        # Formula: (1 + r1) * (1 + r2) ... - 1
        get_cumulative_returns_in_trades_only = self.get_cumulative_returns_in_trades_only()
        
        plt.figure(figsize=(12, 6))
        
        # Plot cumulative returns
        plt.plot(get_cumulative_returns_in_trades_only.index, get_cumulative_returns_in_trades_only.values, label='Cumulative Returns', color='blue', linewidth=2)
        
        # Fill under the curve
        plt.fill_between(get_cumulative_returns_in_trades_only.index, get_cumulative_returns_in_trades_only.values, alpha=0.2, color='blue')
        
        # Horizontal line at 0
        plt.axhline(0, color='black', linestyle='--', linewidth=1)
        
        plt.title(title, fontsize=14)
        plt.xlabel('Trade Index / Time', fontsize=12)
        plt.ylabel('Cumulative Return', fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.legend()
        
        # Adjust layout
        plt.tight_layout()

        plt.show()
        
        # Save the figure
        #plt.savefig('strategy_returns_plot.png')


    def plot_strategy_returns_in_trades_only_with_parameters(self, params_dict, title="Cumulative Strategy Returns per Trade"):
        """
        Plots the cumulative returns with a dynamic parameter box.
        
        Args:
            params_dict (dict): Dictionary containing the parameter names and values.
            title (str): Title of the plot.
        """
        # 1. Fetch data
        get_cumulative_returns_in_trades_only = self.get_cumulative_returns_in_trades_only()
        
        plt.figure(figsize=(12, 7))
        
        # 2. Plotting logic
        plt.plot(get_cumulative_returns_in_trades_only.index, 
                get_cumulative_returns_in_trades_only.values, 
                label='Cumulative Returns', color='blue', linewidth=2)
        
        plt.fill_between(get_cumulative_returns_in_trades_only.index, 
                        get_cumulative_returns_in_trades_only.values, 
                        alpha=0.2, color='blue')
        
        plt.axhline(0, color='black', linestyle='--', linewidth=1)

        # 3. Construct params_info string dynamically from the input dictionary
        # This loop formats each key-value pair and joins them with newlines
        params_str = "\n".join([f"{k}: {v}" for k, v in params_dict.items()])

        # 4. Add the text box (Legend-style)
        # Using 'monospace' ensures the colons align if keys are similar lengths
        props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
        
        plt.gca().text(0.02, 0.95, params_str, transform=plt.gca().transAxes, 
                    fontsize=9, verticalalignment='top', bbox=props, family='monospace')

        # 5. Final Styling
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Cumulative Return', fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()
        #plt.savefig()