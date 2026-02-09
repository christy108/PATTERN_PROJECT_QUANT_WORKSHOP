import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



class Evaluate_Strategy:

    
    #Can add date too for plotting
    def __init__(self, asset_returns, strategy_returns_in_trades_only, all_strategy_returns):
        self.strategy_returns_in_trades_only = pd.Series(strategy_returns_in_trades_only)
        self.all_strategy_returns = pd.Series(all_strategy_returns)
        self.asset_returns = pd.Series(asset_returns)
        
        
    

    def get_cumulative_returns_in_trades_only(self):
        cum_ret = (1 + self.strategy_returns_in_trades_only).cumprod() - 1

        return cum_ret*100

    
    def get_cumulative_returns_all_strategy(self):
        cum_ret = (1 + self.all_strategy_returns).cumprod() - 1
        return cum_ret*100
    
    def get_cumulative_return_original_asset(self):
        cum_ret = (1+ self.asset_returns).cumprod() - 1
        return cum_ret*100
    

    def get_sharpe_ratio_in_trade_only(self):
        """
        Calculates the annualized Sharpe Ratio from daily returns.

        """

        risk_free_rate=0
        trading_days=252

        # Convert annual risk-free rate to daily
        daily_rf = (1 + risk_free_rate) ** (1 / trading_days) - 1
        
        # Calculate excess returns
        excess_returns = self.strategy_returns_in_trades_only - daily_rf
        
        # Calculate mean and standard deviation of excess returns
        mean_excess_return = np.mean(excess_returns)
        std_dev_returns = np.std(excess_returns)
        
        # Calculate daily Sharpe Ratio
        daily_sharpe = mean_excess_return / std_dev_returns
        
        # Annualize the Sharpe Ratio
        annualized_sharpe = daily_sharpe * np.sqrt(trading_days)
        
        return annualized_sharpe
    


    def get_sharpe_ratio_all_strategy(self):
        """
        Calculates the annualized Sharpe Ratio from daily returns.
        """
        risk_free_rate=0
        trading_days=252

        # Convert annual risk-free rate to daily
        daily_rf = (1 + risk_free_rate) ** (1 / trading_days) - 1
        
        # Calculate excess returns
        excess_returns = self.all_strategy_returns - daily_rf
        
        # Calculate mean and standard deviation of excess returns
        mean_excess_return = np.mean(excess_returns)
        std_dev_returns = np.std(excess_returns)
        
        # Calculate daily Sharpe Ratio
        daily_sharpe = mean_excess_return / std_dev_returns
        
        # Annualize the Sharpe Ratio
        annualized_sharpe = daily_sharpe * np.sqrt(trading_days)
        
        return annualized_sharpe
    
    def get_sharpe_ratio_original_asset(self):
        """
        Calculates the annualized Sharpe Ratio for the original underlying asset.
        """
        risk_free_rate = 0
        trading_days = 252

        # Convert annual risk-free rate to daily
        daily_rf = (1 + risk_free_rate) ** (1 / trading_days) - 1
        
        # Calculate excess returns
        excess_returns = self.asset_returns - daily_rf
        
        # Calculate stats using NumPy for speed
        mean_excess_return = np.mean(excess_returns)
        std_dev_returns = np.std(excess_returns)
        
        # Avoid division by zero if asset had no volatility
        if std_dev_returns == 0:
            return 0
            
        daily_sharpe = mean_excess_return / std_dev_returns
        
        # Annualize
        return daily_sharpe * np.sqrt(trading_days)



    ####PLOTSSSS START HERE######

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



    def plot_strategy_returns_all_strategy_with_parameters(self, params_dict, title="Cumulative Strategy Returns per Trade"):
        """
        Plots the cumulative returns with a dynamic parameter box.
        
        Args:
            params_dict (dict): Dictionary containing the parameter names and values.
            title (str): Title of the plot.
        """
        # 1. Fetch data
        get_cumulative_returns = self.get_cumulative_returns_all_strategy()
        
        plt.figure(figsize=(12, 7))
        
        # 2. Plotting logic
        plt.plot(get_cumulative_returns.index, 
                get_cumulative_returns.values, 
                label='Cumulative Returns', color='blue', linewidth=2)
        
        plt.fill_between(get_cumulative_returns.index, 
                        get_cumulative_returns.values, 
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


    
    def plot_original_asset_returns_with_parameters(self, sharpe_ratio, title="Cumulative Asset Returns"):
        """
        Plots the cumulative returns with only the Sharpe Ratio in the legend.
        
        Args:
            sharpe_ratio (float/str): The calculated Sharpe Ratio value.
            title (str): Title of the plot.
        """
        # 1. Fetch data
        get_cumulative_returns = self.get_cumulative_return_original_asset()
        
        # 2. Format the label for the legend
        # If it's a number, format to 4 decimal places; if not, just use the string.
        if isinstance(sharpe_ratio, (int, float)):
            label_text = f'Cumulative Returns (Sharpe: {sharpe_ratio:.4f})'
        else:
            label_text = f'Cumulative Returns (Sharpe: {sharpe_ratio})'
        
        plt.figure(figsize=(12, 7))
        
        # 3. Plotting logic
        plt.plot(get_cumulative_returns.index, 
                get_cumulative_returns.values, 
                label=label_text, color='blue', linewidth=2)
        
        plt.fill_between(get_cumulative_returns.index, 
                        get_cumulative_returns.values, 
                        alpha=0.2, color='blue')
        
        plt.axhline(0, color='black', linestyle='--', linewidth=1)

        # 4. Styling
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Cumulative Return (%)', fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        # Legend will now only show the label defined in step 2
        plt.legend(loc='upper left', fontsize=10)
        
        plt.tight_layout()
        plt.show()



    def plot_dynamic_betsize(self, betsize_list):
        """
        Initializes betsize_list as a pandas Series and plots the percentage 
        of portfolio invested per trade with a bright green line and a mean reference.
        """
        # 1. Initialize data
        self.betsize_list = pd.Series(betsize_list)
        mean_val = self.betsize_list.mean()
        
        # 2. Setup Figure
        plt.figure(figsize=(12, 7))
        
        # 3. Plotting logic
        # Using 'lime' or '#00FF00' for that bright green look
        plt.plot(self.betsize_list.index, 
                self.betsize_list.values, 
                label='Bet Size per Trade', 
                color='lime', 
                linewidth=2)
        
        # Add the mean line
        plt.axhline(mean_val, 
                    color='red', 
                    linestyle='--', 
                    linewidth=1.5, 
                    label=f'Mean Bet Size: {mean_val:.2f}%')
        
        # Horizontal line at 0 for baseline
        plt.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)

        # 4. Styling
        # Setting a slightly darker background often makes bright green pop better
        # plt.gca().set_facecolor('#2b2b2b') # Uncomment if you want a dark 'terminal' look
        
        plt.title('Percentage of Portfolio Invested per Trade', fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Portfolio Invested (%)', fontsize=12)
        
        plt.grid(True, which='both', linestyle='--', alpha=0.3)
        plt.legend(loc='upper left', fontsize=10)
        
        plt.tight_layout()
        plt.show()

