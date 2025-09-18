"""
Main Orchestration for Risk Analytics Platform
Industry-ready: integrates risk, stress, and reporting modules
"""

import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

# Local imports
from risk_analytics.utils import load_config, ensure_dirs, try_git_commit_hash, sha256
from risk_analytics.risk_models import calculate_var_es, calculate_drawdowns, calculate_performance
from risk_analytics.stress import sector_shock_impact, rates_shock_impact, volatility_shock_impact
from risk_analytics.reporting import (
    save_var_results,
    save_strategy_results,
    save_exposures,
    save_drawdowns,
    save_performance,
    save_stress_summary,
    save_audit_log,
    save_csvs,
    save_plots,
)

# --------------------------------------
# Logging Setup
# --------------------------------------
logger = logging.getLogger("risk_analytics.main")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    try:
        # ==========================
        # 1. Load Config
        # ==========================
        project_root = Path(__file__).resolve().parents[2]
        cfg_path = project_root / "configs" / "risk_config.yaml"
        config = load_config(str(cfg_path))

        output_dir = project_root / config["reporting"]["output_dir"]
        ensure_dirs(output_dir)

        logger.info(f"✅ Config loaded from {cfg_path}")

        # ==========================
        # 2. Load Data
        # ==========================
        trading_file = project_root / config["data"]["trading_file"]
        instruments_file = project_root / config["data"]["instruments_file"]

        trades = pd.read_csv(trading_file, parse_dates=[config["data"]["timestamp_column"]])
        instruments = pd.read_csv(instruments_file)

        # Merge enriched dataset
        df = pd.merge(trades, instruments, on=config["data"]["instrument_column"], how="left")
        df.sort_values(config["data"]["timestamp_column"], inplace=True)
        df["date"] = pd.to_datetime(df[config["data"]["timestamp_column"]]).dt.date

        logger.info(f" Trading shape={trades.shape} | Instruments shape={instruments.shape}")
        logger.info(f" Merged shape={df.shape}")

        # Portfolio NAV Series
        initial_nav = config["portfolio"]["initial_nav"]
        pnl_col = config["data"]["pnl_column"]
        daily_pnl = df.groupby("date")[pnl_col].sum()
        nav_series = initial_nav + daily_pnl.cumsum()

        logger.info(f" Initial NAV: ${initial_nav:,.2f} (source=config)")

        # ==========================
        # 3. Daily Returns
        # ==========================
        daily_return = nav_series.pct_change().fillna(0.0)

        # ==========================
        # 4. Portfolio Risk Metrics
        # ==========================
        var_results = calculate_var_es(
            df[pnl_col], levels=config["risk"]["var_levels"]
        )
        drawdowns_df = calculate_drawdowns(nav_series)
        performance = calculate_performance(
            nav_series,
            risk_free_rate=config["performance"]["risk_free_rate"],
        )

        logger.info(f" Portfolio Risk Metrics: {var_results}")

        # ==========================
        # 5. Strategy-Level Results
        # ==========================
        strategy_col = config["data"]["strategy_column"]
        strategy_results = {}

        if strategy_col in df.columns:
            for strat, group in df.groupby(strategy_col):
                strat_pnl = group.groupby("date")[pnl_col].sum()
                strat_nav = (initial_nav / len(df[strategy_col].unique())) + strat_pnl.cumsum()
                strategy_results[strat] = calculate_performance(
                    strat_nav,
                    risk_free_rate=config["performance"]["risk_free_rate"],
                )

        logger.info(f" Strategy-level performance computed: {list(strategy_results.keys())}")

        # ==========================
        # 6. Exposures (sector/instrument)
        # ==========================
        exposures = {}
        if "sector" in df.columns:
            exposures["sector"] = df.groupby("sector")[pnl_col].sum().to_dict()
        if config["data"]["instrument_column"] in df.columns:
            exposures["instrument"] = df.groupby(config["data"]["instrument_column"])[pnl_col].sum().to_dict()

        # ==========================
        # 7. Stress Testing
        # ==========================
        stress_results = {}
        if config["stress_scenarios"]["enabled"]:
            for name, s in config["stress_scenarios"]["scenarios"].items():
                if s["type"] == "sector":
                    stress_results[name] = sector_shock_impact(
                        df,
                        s["sector_col"],
                        s["target_sector"],
                        s["shock_pct"],
                        nav_series,
                    )
                elif s["type"] == "rates":
                    stress_results[name] = rates_shock_impact(
                        df,
                        s["delta_bps"],
                        s["proxy_duration_col"],
                        nav_series,
                        config["mappings"]["duration_from_credit_rating"],
                        config["mappings"]["default_duration"],
                    )
                elif s["type"] == "vol":
                    stress_results[name] = volatility_shock_impact(
                        df,
                        s["vol_col"],
                        s["vol_mult"],
                        nav_series,
                    )

        logger.info(f" Stress Test Results: {stress_results}")

        # ==========================
        # 8. Alerts (Risk Thresholds)
        # ==========================
        alerts = []
        var_limit = config["risk"]["var_alert_usd"]
        dd_limit = config["risk"]["drawdown_alert_pct"]

        if any(v is not None and v < -var_limit for v in var_results.values() if isinstance(v, (int, float))):
            alerts.append("⚠️ Portfolio VaR breach detected")

        if not drawdowns_df.empty and drawdowns_df["drawdown"].min() < -dd_limit:
            alerts.append("⚠️ Portfolio drawdown limit breached")

        if alerts:
            logger.warning(f" Alerts triggered: {alerts}")

        # ==========================
        # 9. Reporting
        # ==========================
        save_var_results(var_results, output_dir)
        save_strategy_results(strategy_results, output_dir)
        save_exposures(exposures, output_dir)
        save_drawdowns(drawdowns_df, output_dir)
        save_performance(performance, output_dir)
        save_stress_summary(stress_results, output_dir)

        # Rolling Sharpe
        rf_daily = config["performance"]["risk_free_rate"] / config["performance"]["annualization_factor"]
        rolling_sharpe = (
            (daily_return - rf_daily).rolling(config["performance"]["sharpe_window"]).mean()
            / daily_return.rolling(config["performance"]["sharpe_window"]).std().replace(0, 1e-12)
        )
        rolling_sharpe *= np.sqrt(config["performance"]["annualization_factor"])

        # Save CSVs + Plots
        save_csvs(
            daily_pnl=daily_pnl,
            daily_return=daily_return,
            strat_returns={strat: group.groupby("date")[pnl_col].sum()
                           for strat, group in df.groupby(strategy_col)},
            out_dir=output_dir
        )
        save_plots(
            daily_pnl=daily_pnl,
            cum_returns=nav_series / initial_nav - 1,
            rolling_sharpe=rolling_sharpe,
            drawdown=drawdowns_df.set_index("date")["drawdown"],
            out_dir=output_dir,
            sharpe_window=config["performance"]["sharpe_window"],
        )

        # ==========================
        # 10. Audit Log
        # ==========================
        audit_data = {
            "run_time": datetime.utcnow().isoformat() + "Z",
            "git_commit": try_git_commit_hash(),
            "snapshots": {
                "trading_csv": sha256(str(trading_file)),
                "instruments_csv": sha256(str(instruments_file)),
            },
            "config": config,
            "portfolio_var": var_results,
            "strategy_results": strategy_results,
            "exposures": exposures,
            "performance": performance,
            "stress_results": stress_results,
            "alerts": alerts,
            "latest_nav": float(nav_series.iloc[-1]),
        }
        save_audit_log(audit_data, output_dir)

        logger.info("✅ Risk Analytics Pipeline Completed Successfully")

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
