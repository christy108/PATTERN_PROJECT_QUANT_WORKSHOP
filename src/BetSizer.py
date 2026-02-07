import numpy as np

def kelly_bet_size(expected_return, predicted_vol, kelly_fraction=0.15, max_bet=1.0):
    """
    Compute a bet size between 0 and 1 using a Kelly-style fraction,
    inversely proportional to predicted volatility.

    Parameters
    ----------
    expected_return : float
        Expected return of the trade (decimal, e.g., 0.001 = 0.1%)
    predicted_vol : float
        Predicted daily volatility (decimal, e.g., 0.01 = 1%)
    kelly_fraction : float
        Fraction of full Kelly to use (default 0.15)
    max_bet : float
        Maximum bet size (default 1.0)

    Returns
    -------
    float
        Bet size between 0 and max_bet
    """
    # Avoid division by zero
    if predicted_vol <= 0:
        predicted_vol = 1e-6

    # Classic Kelly: f* = mu / sigma^2
    full_kelly = expected_return / (predicted_vol ** 2)

    # Scale by fraction and clip
    scaled_kelly = kelly_fraction * full_kelly
    bet_size = np.clip(scaled_kelly, 0.0, max_bet)

    return bet_size
