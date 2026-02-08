# bet_size.py

import numpy as np

def bet_size_from_next_day_vol(
    next_day_vol,
    vol_history,
    max_bet_fraction=0.05,
    z_clip=2.5
):
    """
    Compute bet size based on next-day volatility using Z-score normalization.

    Parameters
    ----------
    next_day_vol : float
        Predicted next-day volatility (decimal, e.g., 0.02 = 2%)
    vol_history : array-like
        Array of past predicted next-day volatilities (rolling window)
    max_bet_fraction : float, optional
        Maximum allowed bet size (default 0.05 = 5%)
    z_clip : float, optional
        Maximum Z-score for clipping to avoid extremes (default 2.5)

    Returns
    -------
    float
        Bet size in [0, max_bet_fraction]
    """
    vol_history = np.array(vol_history)
    mean_vol = np.mean(vol_history)
    std_vol = np.std(vol_history)

    if std_vol == 0:
        return max_bet_fraction * 0.5  # fallback if all vols are the same

    # Z-score of next-day volatility
    z = (next_day_vol - mean_vol) / std_vol
    z = np.clip(z, -z_clip, z_clip)

    # Map z-score to 0–1 range
    normalized_vol = (z + z_clip) / (2 * z_clip)

    # Inverse relation: higher vol → smaller bet
    bet = max_bet_fraction * (1 - normalized_vol)

    # Clamp bet size
    return float(np.clip(bet, 0, max_bet_fraction))
