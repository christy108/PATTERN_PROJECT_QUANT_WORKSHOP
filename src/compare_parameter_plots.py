import matplotlib.pyplot as plt

def plot_comparison(eval1, label1, eval2, label2, title="Strategy Comparison"):
    plt.figure(figsize=(12, 7))
    
    # Get cumulative returns (Percentage)
    cum_ret1 = eval1.get_cumulative_returns_all_strategy()
    cum_ret2 = eval2.get_cumulative_returns_all_strategy()

    sharpe_startegy1 = eval1.get_sharpe_ratio_in_trade_only()
    sharpe_startegy2 = eval2.get_sharpe_ratio_in_trade_only()
    
    # Plot both
    plt.plot(cum_ret1.index, cum_ret1.values, label=label1, linewidth=2)
    plt.plot(cum_ret2.index, cum_ret2.values, label=label2, linewidth=2)
    
    # Styling
    plt.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.7)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time Steps', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()