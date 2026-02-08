import numpy as np
from arch import arch_model

def predict_next_day_volatility(returns, lookback=100):
    """
    GARCH(1,1) next-day volatility forecast.

    returns : np.ndarray of daily returns (decimal)
    lookback : int (rolling window length)

    returns
    -------
    float : next-day volatility (decimal)
    """

    r = returns[-lookback:] * 100  # GARCH expects %
    
    model = arch_model(
        r,
        mean="Zero",
        vol="GARCH",
        p=1,
        q=1,
        dist="normal"
    )

    res = model.fit(disp="off")
    forecast = res.forecast(horizon=1)

    var_next = forecast.variance.iloc[-1, 0] / (100 ** 2)
    return float(np.sqrt(var_next))
