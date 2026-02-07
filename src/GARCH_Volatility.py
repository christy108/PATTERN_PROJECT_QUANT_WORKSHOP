# GARCH_Volatility.py
import yfinance as yf
import numpy as np
from arch import arch_model

def get_garch_volatility(ticker="AAPL", start_date="2022-01-01", end_date="2023-12-31", lookback=300):
    """
    Download stock data and estimate rolling next-day GARCH(1,1) volatility.

    Returns:
    --------
    dates : np.array
        Dates corresponding to predicted volatilities
    predicted_vols : np.array
        Predicted daily volatilities (decimal)
    """
    # Download stock data
    data = yf.download(ticker, start=start_date, end=end_date)[['Close']]
    data['Returns'] = data['Close'].pct_change()
    data = data.dropna()
    all_returns = data['Returns'].to_numpy()
    dates = data.index

    predicted_vols = []

    for i in range(lookback, len(all_returns)):
        returns_window = all_returns[i-lookback:i]
        model = arch_model(returns_window*100, mean="Zero", vol="GARCH", p=1, q=1, dist="normal")
        garch_result = model.fit(disp="off")
        forecast = garch_result.forecast(horizon=1)
        predicted_var = forecast.variance.iloc[-1, 0] / (100.0 ** 2)
        predicted_vol = np.sqrt(predicted_var)
        predicted_vols.append(predicted_vol)

    vol_dates = dates[lookback:]
    return vol_dates, np.array(predicted_vols)

# -------------------------------
# Example usage if run directly
# -------------------------------
if __name__ == "__main__":
    dates, vols = get_garch_volatility()
    print(f"Predicted volatility for last day: {vols[-1]*100:.2f}%")
