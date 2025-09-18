"""
Risk models for portfolio analytics
Includes VaR, Expected Shortfall (ES), drawdowns, and performance metrics
"""

import numpy as np
import pandas as pd


def calculate_var_es(pnl_series: pd.Series, levels=[0.95, 0.99]) -> dict:
    """
    Historical Value-at-Risk (VaR) and Expected Shortfall (ES).
    Returns a dictionary with VaR_xx and ES_xx for each level.
    """
    results = {}
    pnl_clean = pnl_series.dropna()

    if pnl_clean.empty:
        # Return None for all levels if series is empty
        return {**{f"VaR_{int(l*100)}": None for l in levels},
                **{f"ES_{int(l*100)}": None for l in levels}}

    arr = np.array(pnl_clean)

    for level in levels:
        cutoff = np.percentile(arr, (1 - level) * 100)
        var = float(cutoff)
        tail_losses = arr[arr <= cutoff]
        es = float(tail_losses.mean()) if len(tail_losses) > 0 else None
        results[f"VaR_{int(level*100)}"] = var
        results[f"ES_{int(level*100)}"] = es

    return results


def calculate_drawdowns(nav_series: pd.Series) -> pd.DataFrame:
    """
    Compute portfolio drawdowns.
    Returns a DataFrame with date, nav, running_max, and drawdown.
    """
    nav = nav_series.dropna()
    if nav.empty:
        return pd.DataFrame(columns=["date", "nav", "running_max", "drawdown"])

    running_max = nav.cummax()
    drawdowns = (nav - running_max) / running_max

    dd_df = pd.DataFrame({
        "date": nav.index,
        "nav": nav.values,
        "running_max": running_max.values,
        "drawdown": drawdowns.values
    })

    return dd_df


def calculate_performance(nav_series: pd.Series, risk_free_rate=0.0) -> dict:
    """
    Basic performance metrics: Sharpe ratio, CAGR, annualized return, and volatility.
    """
    nav = nav_series.dropna()
    if nav.empty or len(nav) < 2:
        return {
            "annual_return": None,
            "annual_volatility": None,
            "sharpe_ratio": None,
            "cagr": None
        }

    returns = nav.pct_change().dropna()

    # Annualized metrics
    avg_return = returns.mean() * 252
    vol = returns.std() * np.sqrt(252)
    sharpe = (avg_return - risk_free_rate) / vol if vol > 0 else None

    # CAGR
    total_return = nav.iloc[-1] / nav.iloc[0] - 1
    years = (nav.index[-1] - nav.index[0]).days / 365.25
    cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else None

    return {
        "annual_return": float(avg_return),
        "annual_volatility": float(vol),
        "sharpe_ratio": float(sharpe) if sharpe is not None else None,
        "cagr": float(cagr) if cagr is not None else None
    }
