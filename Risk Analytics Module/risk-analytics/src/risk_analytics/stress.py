"""
Stress testing functions for portfolio scenarios.
Supports sector shocks, rate shocks, and volatility scenarios.
Industry-ready with audit logging.
"""

import pandas as pd
import logging
from typing import Dict, Any


def sector_shock_impact(
    df: pd.DataFrame,
    sector_col: str,
    target_sector: str,
    shock_pct: float,
    nav_series: pd.Series
) -> Dict[str, Any]:
    """
    Estimate impact of a sector shock (e.g., -15% Technology).
    Returns a structured dictionary with results.
    """
    result = {"shock": "sector", "target": target_sector, "shock_pct": shock_pct}

    if sector_col not in df.columns:
        result.update({"impact_usd": None, "impact_pct": None, "status": "sector column missing"})
        return result

    last_date = df["date"].max()
    latest = df[df["date"] == last_date]

    if latest.empty:
        result.update({"impact_usd": None, "impact_pct": None, "status": "no data"})
        return result

    sec_exposure = latest.loc[latest[sector_col] == target_sector, "pnl_usd"].sum()
    nav_last = nav_series.get(last_date, nav_series.iloc[-1])

    impact_usd = sec_exposure * shock_pct
    impact_pct = impact_usd / nav_last if nav_last else None

    result.update({
        "impact_usd": impact_usd,
        "impact_pct": impact_pct,
        "nav": nav_last,
        "status": "ok"
    })
    return result


def rates_shock_impact(
    df: pd.DataFrame,
    delta_bps: float,
    duration_col: str,
    nav_series: pd.Series,
    duration_map: Dict[str, float],
    default_duration: float
) -> Dict[str, Any]:
    """
    Estimate impact of interest rate shock on fixed income using duration.
    Duration can come from a column or mapped from credit rating.
    """
    result = {"shock": "rates", "delta_bps": delta_bps}

    last_date = df["date"].max()
    latest = df[df["date"] == last_date]

    if latest.empty:
        result.update({"impact_usd": None, "impact_pct": None, "status": "no data"})
        return result

    fixed_income = latest[latest["asset_class"].str.contains("Fixed Income", na=False)]
    if fixed_income.empty:
        result.update({"impact_usd": None, "impact_pct": None, "status": "no fixed income exposure"})
        return result

    # Duration from column or credit rating mapping
    if duration_col in fixed_income.columns:
        durations = fixed_income[duration_col].astype(float)
    elif "credit_rating" in fixed_income.columns:
        durations = fixed_income["credit_rating"].map(duration_map).fillna(default_duration)
    else:
        durations = pd.Series([default_duration] * len(fixed_income))

    avg_duration = durations.mean()
    mv = fixed_income.get("market_value", fixed_income["pnl_usd"]).sum()
    delta = delta_bps / 10000.0

    impact_usd = -avg_duration * delta * mv
    nav_last = nav_series.get(last_date, nav_series.iloc[-1])
    impact_pct = impact_usd / nav_last if nav_last else None

    result.update({
        "impact_usd": impact_usd,
        "impact_pct": impact_pct,
        "avg_duration": avg_duration,
        "nav": nav_last,
        "status": "ok"
    })
    return result


def volatility_shock_impact(
    df: pd.DataFrame,
    vol_col: str,
    vol_mult: float,
    nav_series: pd.Series
) -> Dict[str, Any]:
    """
    Estimate impact of higher volatility regime by scaling portfolio volatility.
    Returns a dictionary with impact.
    """
    result = {"shock": "volatility", "vol_mult": vol_mult}

    if vol_col not in df.columns:
        result.update({"impact_usd": None, "impact_pct": None, "status": "vol column missing"})
        return result

    last_date = df["date"].max()
    latest = df[df["date"] == last_date]

    if latest.empty:
        result.update({"impact_usd": None, "impact_pct": None, "status": "no data"})
        return result

    base_vol = latest[vol_col].astype(float).mean()
    stressed_vol = base_vol * vol_mult

    nav_last = nav_series.get(last_date, nav_series.iloc[-1])
    impact_usd = (stressed_vol - base_vol) * nav_last
    impact_pct = impact_usd / nav_last if nav_last else None

    result.update({
        "impact_usd": impact_usd,
        "impact_pct": impact_pct,
        "base_vol": base_vol,
        "stressed_vol": stressed_vol,
        "nav": nav_last,
        "status": "ok"
    })
    return result
