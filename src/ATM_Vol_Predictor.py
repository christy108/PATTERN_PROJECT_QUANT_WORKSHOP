import numpy as np
from arch import arch_model


class ATMVolPredictor:
    """
    Predicts next-day ATM volatility using:
    - VIX as the market-implied anchor
    - GARCH as the time-series volatility dynamics

    Output:
    -------
    Predicted ATM volatility (or variance), suitable for:
      - SVI ATM anchoring
      - volatility surface construction
      - risk and pricing models
    """

    def __init__(
        self,
        garch_p=1,
        garch_q=1,
        dist="normal",
        refit_interval=5,
        trading_days=252
    ):
        self.p = garch_p
        self.q = garch_q
        self.dist = dist
        self.refit_interval = refit_interval
        self.trading_days = trading_days

        self._counter = 0
        self._garch_result = None

    # ------------------------------------------------------------------
    # GARCH fitting and forecasting
    # ------------------------------------------------------------------

    def _fit_garch(self, returns_window):
        """
        Fit GARCH on historical returns
        """
        r = returns_window * 100.0  # arch expects % returns

        model = arch_model(
            r,
            mean="Zero",
            vol="GARCH",
            p=self.p,
            q=self.q,
            dist=self.dist
        )

        self._garch_result = model.fit(disp="off")

    def _forecast_garch_daily_variance(self, returns_window):
        """
        Forecast next-day variance from GARCH
        """
        self._counter += 1

        if (
            self._garch_result is None
            or self._counter % self.refit_interval == 0
        ):
            self._fit_garch(returns_window)

        forecast = self._garch_result.forecast(horizon=1)
        var_1d = forecast.variance.iloc[-1, 0] / (100.0 ** 2)

        return var_1d

    # ------------------------------------------------------------------
    # VIX processing
    # ------------------------------------------------------------------

    def vix_to_daily_variance(self, vix_level):
        """
        Convert VIX (annualized 30-day vol) into daily variance
        """
        annual_var = (vix_level / 100.0) ** 2
        daily_var = annual_var / self.trading_days
        return daily_var

    # ------------------------------------------------------------------
    # PUBLIC API: volatility prediction
    # ------------------------------------------------------------------

    def predict_atm_volatility(
        self,
        returns_window,
        vix_level,
        weight_vix=0.6,
        output="vol"
    ):
        """
        Predict next-day ATM volatility.

        Parameters
        ----------
        returns_window : np.ndarray
            Recent daily returns (decimal)
        vix_level : float
            Current VIX level
        weight_vix : float in [0,1]
            Weight on VIX vs GARCH
        output : str
            'vol' or 'var'

        Returns
        -------
        float
            Predicted ATM volatility or variance
        """

        garch_var = self._forecast_garch_daily_variance(returns_window)
        vix_var = self.vix_to_daily_variance(vix_level)

        atm_var = (
            weight_vix * vix_var
            + (1.0 - weight_vix) * garch_var
        )

        if output == "var":
            return atm_var
        elif output == "vol":
            return np.sqrt(atm_var)
        else:
            raise ValueError("output must be 'vol' or 'var'")
