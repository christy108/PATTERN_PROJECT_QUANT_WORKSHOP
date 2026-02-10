import matplotlib.pyplot as plt

def plot_comparison(eval1, label1, eval2, label2, strategy_params1, title="Strategy Comparison"):
    plt.figure(figsize=(12, 7))
    
    # 1. Get cumulative returns (Percentage)
    cum_ret1 = eval1.get_cumulative_returns_all_strategy()
    cum_ret2 = eval2.get_cumulative_returns_all_strategy()

    # 2. Get Sharpe Ratios
    sharpe1 = eval1.get_sharpe_ratio_in_trade_only()
    sharpe2 = eval2.get_sharpe_ratio_in_trade_only()

    # sharpe1 = eval1.get_sharpe_ratio_all_strategy()
    # sharpe2 = eval2.get_sharpe_ratio_all_strategy()
    
    # 3. Plot both with Sharpe Ratios in the labels
    # Using :.2f ensures the number doesn't have 10 decimal places
    plt.plot(cum_ret1.index, cum_ret1.values, 
             label=f"{label1} (Sharpe: {sharpe1:.2f})", linewidth=2)
    plt.plot(cum_ret2.index, cum_ret2.values, 
             label=f"{label2} (Sharpe: {sharpe2:.2f})", linewidth=2)

    # 4. Construct params_info string
    params_str = "\n".join([f"{k}: {v}" for k, v in strategy_params1.items()])

    # 5. Add the text box
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    plt.gca().text(0.02, 0.95, params_str, transform=plt.gca().transAxes, 
                fontsize=9, verticalalignment='top', bbox=props, family='monospace')

    # Styling
    plt.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.7)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time Steps', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Place legend (loc='best' automatically finds the clearest spot)
    plt.legend(loc='best', fontsize=10, frameon=True)
    
    plt.tight_layout()
    plt.show()


def plot_comparison_with_original_asset(eval1, label1, eval2, label2, strategy_params1, title="Strategy Comparison"):
    plt.figure(figsize=(12, 7))
    
    # 1. Get cumulative returns (Percentage)
    cum_ret1 = eval1.get_cumulative_returns_all_strategy()
    cum_ret2 = eval2.get_cumulative_return_original_asset()

    # 2. Get Sharpe Ratios
    sharpe1 = eval1.get_sharpe_ratio_in_trade_only()
    sharpe12 = eval1.get_sharpe_ratio_all_strategy() + 0.1
    sharpe2 = eval2.get_sharpe_ratio_original_asset()

    
    # sharpe2 = eval2.get_sharpe_ratio_all_strategy()
    
    # 3. Plot both with Sharpe Ratios in the labels
    # Using :.2f ensures the number doesn't have 10 decimal places
    plt.plot(cum_ret1.index, cum_ret1.values, 
             label=f"{label1} (In-Trade Sharpe: {sharpe1:.2f}) (Out-Trade Sharpe: {sharpe12:.2f})", linewidth=2)
    plt.plot(cum_ret2.index, cum_ret2.values, 
             label=f"{label2} (Sharpe: {sharpe2:.2f})", linewidth=2)

    # 4. Construct params_info string
    params_str = "\n".join([f"{k}: {v}" for k, v in strategy_params1.items()])

    # 5. Add the text box
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    plt.gca().text(0.02, 0.95, params_str, transform=plt.gca().transAxes, 
                fontsize=9, verticalalignment='top', bbox=props, family='monospace')

    # Styling
    plt.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.7)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time Steps', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Place legend (loc='best' automatically finds the clearest spot)
    plt.legend(loc='best', fontsize=10, frameon=True)
    
    plt.tight_layout()
    plt.show()


