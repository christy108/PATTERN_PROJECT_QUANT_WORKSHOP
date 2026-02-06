import numpy as np

def get_bet_size(
    predicted_probability: float,
    predicted_volatility: float,
    reference_volatility: float,
    kelly_fraction: float = 0.15,
    max_bet_size: float = 0.05
) -> float:
    """
    Calculates position size using fractional Kelly penalized by volatility.

    Parameters
    ----------
    predicted_probability : float
        Probability of correct direction (0 to 1)

    predicted_volatility : float
        Forecasted volatility (e.g. std of returns)

    reference_volatility : float
        Baseline volatility (rolling mean or long-run avg)

    kelly_fraction : float
        Fraction of Kelly to use (default 15%)

    max_bet_size : float
        Hard cap on position size (risk control)

    Returns
    -------
    float
        Bet size as fraction of capital (positive = long, negative = short)
    """

    # Kelly signal (binary outcome)
    kelly_signal = 2.0 * predicted_probability - 1.0
    kelly_size = kelly_fraction * kelly_signal

    # Volatility penalty (higher vol -> smaller size)
    vol_penalty = 1.0 / (1.0 + predicted_volatility / reference_volatility)

    # Final bet size
    bet_size = kelly_size * vol_penalty

    # Risk cap
    bet_size = np.clip(bet_size, -max_bet_size, max_bet_size)

    return bet_size
