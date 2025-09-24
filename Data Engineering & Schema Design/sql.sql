-- -------------------------
-- Raw Layer (staging tables)
-- -------------------------
CREATE TABLE raw_instruments (
  instrument_id VARCHAR(50),
  symbol VARCHAR(20),
  instrument_name VARCHAR(100),
  asset_class VARCHAR(50),
  exchange VARCHAR(50),
  sector VARCHAR(50),
  market_cap_usd DECIMAL(20,2),
  avg_daily_volume DECIMAL(20,2),
  beta DOUBLE,
  volatility_30d DOUBLE,
  sharpe_ratio DOUBLE,
  correlation_to_index DOUBLE,
  dividend_yield DOUBLE,
  pe_ratio DOUBLE,
  debt_to_equity DOUBLE,
  updated_at DATETIME
);

CREATE TABLE raw_trading (
  trade_id VARCHAR(50),
  trade_timestamp DATETIME,
  instrument_id VARCHAR(50),
  order_id VARCHAR(50),
  strategy_id VARCHAR(50),
  order_type VARCHAR(20),
  side VARCHAR(10),
  quantity BIGINT,
  price DECIMAL(20,6),
  execution_price DECIMAL(20,6),
  slippage_bps DECIMAL(10,4),
  commission_usd DECIMAL(20,6),
  market_impact_bps DECIMAL(10,4),
  pnl_usd DECIMAL(20,6),
  unrealized_pnl_usd DECIMAL(20,6),
  position_size DECIMAL(20,6),
  portfolio_weight DECIMAL(10,6),
  var_contribution DECIMAL(20,6),
  expected_shortfall DECIMAL(20,6),
  alpha DECIMAL(20,6),
  information_ratio DECIMAL(20,6),
  venue VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------
-- Curated Layer (dim/fact)
-- -------------------------
CREATE TABLE dim_instrument (
  instrument_id VARCHAR(50) PRIMARY KEY,
  symbol VARCHAR(20),
  instrument_name VARCHAR(100),
  asset_class VARCHAR(50),
  exchange VARCHAR(50),
  sector VARCHAR(50),
  market_cap_usd DECIMAL(20,2),
  avg_daily_volume DECIMAL(20,2),
  beta DOUBLE,
  volatility_30d DOUBLE,
  sharpe_ratio DOUBLE,
  correlation_to_index DOUBLE,
  dividend_yield DOUBLE,
  pe_ratio DOUBLE,
  debt_to_equity DOUBLE,
  updated_at DATETIME
);

CREATE TABLE fact_trade (
  trade_id VARCHAR(50) PRIMARY KEY,
  trade_timestamp DATETIME,
  instrument_id VARCHAR(50),
  strategy_id VARCHAR(50),
  side ENUM('BUY','SELL'),
  quantity BIGINT,
  execution_price DECIMAL(20,6),
  pnl_usd DECIMAL(20,6),
  var_contribution DECIMAL(20,6),
  expected_shortfall DECIMAL(20,6),
  commission_usd DECIMAL(20,6),
  slippage_bps DECIMAL(10,4),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (instrument_id) REFERENCES dim_instrument(instrument_id)
);

-- -------------------------
-- Reporting Layer (aggregated facts)
-- -------------------------
CREATE TABLE rpt_daily_risk (
  snapshot_date DATE,
  portfolio_id VARCHAR(50),
  var_95 DECIMAL(20,6),
  var_99 DECIMAL(20,6),
  es_95 DECIMAL(20,6),
  es_99 DECIMAL(20,6),
  total_pnl DECIMAL(20,6),
  exposure_sector JSON,
  PRIMARY KEY (snapshot_date, portfolio_id)
);

CREATE TABLE rpt_tca_summary (
  week_start DATE,
  portfolio_id VARCHAR(50),
  avg_slippage_bps DECIMAL(10,4),
  total_commission_usd DECIMAL(20,6),
  market_impact_bps DECIMAL(10,4),
  PRIMARY KEY (week_start, portfolio_id)
);
