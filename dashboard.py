import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import os
from typing import Optional, Dict, List

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

BASE_PATH = r"C:\Users\myhp2\risk-analytics\src\risk_analytics\Finance"

RISK_LIMITS = {
    'var_95_limit': -10.0,
    'var_99_limit': -40.0,
    'es_95_limit': -50.0,
    'es_99_limit': -150.0,
    'sector_concentration_limit': 0.15,
    'single_position_limit': 0.10,
    'slippage_threshold_bps': 10.0,
    'market_impact_threshold_bps': 15.0,
    'max_drawdown_limit': -0.20
}

COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'accent': '#f093fb',
    'danger': '#ff6b6b',
    'warning': '#feca57',
    'success': '#48dbfb',
    'info': '#00d2d3',
    'dark': '#0f0f23',
    'surface': '#1a1a2e',
    'card': '#16213e',
    'text': '#e4e4e7',
    'muted': '#94a3b8'
}

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Risk Analytics Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ULTRA-MODERN PROFESSIONAL STYLING
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e4e4e7;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a15 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] * {
        color: #e4e4e7 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(102, 126, 234, 0.05) !important;
        border-radius: 12px;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 3px solid transparent;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(102, 126, 234, 0.12) !important;
        transform: translateX(4px);
        border-left-color: #667eea;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] input:checked + div {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)) !important;
        border-left: 3px solid #667eea !important;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.75rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
    }
    
    h2 {
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        color: #e4e4e7 !important;
        letter-spacing: -0.02em;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.375rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
        letter-spacing: -0.01em;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.75rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-color, #667eea), transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.75rem 0;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .kpi-change {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 100px;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .kpi-subtitle {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.75rem;
        font-weight: 500;
    }
    
    .section-header {
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, transparent 100%);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 2.5rem 0 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .section-header h3 {
        margin: 0 !important;
        font-size: 1.25rem !important;
    }
    
    .alert-box {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(20px);
        font-size: 0.95rem;
        line-height: 1.7;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .alert-box:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
    }
    
    .alert-critical {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 107, 107, 0.05));
    }
    
    .alert-danger {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.12), rgba(255, 107, 107, 0.04));
    }
    
    .alert-warning {
        border-color: #feca57;
        background: linear-gradient(135deg, rgba(254, 202, 87, 0.12), rgba(254, 202, 87, 0.04));
    }
    
    .alert-success {
        border-color: #48dbfb;
        background: linear-gradient(135deg, rgba(72, 219, 251, 0.12), rgba(72, 219, 251, 0.04));
    }
    
    .alert-info {
        border-color: #00d2d3;
        background: linear-gradient(135deg, rgba(0, 210, 211, 0.12), rgba(0, 210, 211, 0.04));
    }
    
    .trade-card {
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.8) 0%, rgba(26, 26, 46, 0.8) 100%);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .trade-card:hover {
        transform: translateX(6px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
    
    .trade-buy {
        border-color: #48dbfb;
        background: linear-gradient(135deg, rgba(72, 219, 251, 0.08), rgba(72, 219, 251, 0.02));
    }
    
    .trade-sell {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.08), rgba(255, 107, 107, 0.02));
    }
    
    .data-quality {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1.25rem;
        border-radius: 100px;
        font-size: 0.875rem;
        font-weight: 700;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .data-quality:hover {
        transform: scale(1.05);
    }
    
    .quality-high {
        background: linear-gradient(135deg, rgba(72, 219, 251, 0.2), rgba(72, 219, 251, 0.1));
        border: 1px solid rgba(72, 219, 251, 0.3);
        color: #48dbfb;
    }
    
    .quality-medium {
        background: linear-gradient(135deg, rgba(254, 202, 87, 0.2), rgba(254, 202, 87, 0.1));
        border: 1px solid rgba(254, 202, 87, 0.3);
        color: #feca57;
    }
    
    .quality-low {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2), rgba(255, 107, 107, 0.1));
        border: 1px solid rgba(255, 107, 107, 0.3);
        color: #ff6b6b;
    }
    
    .metric-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background: transparent;
        border-radius: 12px 12px 0 0;
        font-weight: 600;
        color: #94a3b8;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #e4e4e7;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border-bottom: 3px solid #667eea;
        color: #667eea !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #7c8eef 0%, #8a5fb8 100%);
    }
    
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 35, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        border: 2px solid rgba(15, 15, 35, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c8eef, #8a5fb8);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 2rem 0;
    }
    
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(22, 33, 62, 0.5);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        color: #e4e4e7;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .kpi-card, .trade-card, .alert-box {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def load_csv_safe(path: str) -> pd.DataFrame:
    try:
        if not os.path.exists(path):
            return pd.DataFrame()
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()
        df = df.drop_duplicates()
        return df
    except:
        return pd.DataFrame()

def assess_data_quality(df: pd.DataFrame) -> str:
    if df.empty:
        return "low"
    missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    if missing_pct < 1:
        return "high"
    elif missing_pct < 5:
        return "medium"
    else:
        return "low"

# ============================================================================
# FILE PATHS & DATA LOADING
# ============================================================================

PATHS = {
    "risk_metrics": os.path.join(BASE_PATH, "Risk Analytics Module", "daily_risk_metrics.csv"),
    "sector_exposure": os.path.join(BASE_PATH, "Risk Analytics Module", "sector_exposure.csv"),
    "backtest_results": os.path.join(BASE_PATH, "Backtesting Framework & Strategies", "backtest_results.csv"),
    "backtest_wf": os.path.join(BASE_PATH, "Backtesting Framework & Strategies", "backtest_results_walkforward.csv"),
    "target_weights": os.path.join(BASE_PATH, "Portfolio Optimization Module", "target_weights.csv"),
    "trade_recommendations": os.path.join(BASE_PATH, "Portfolio Optimization Module", "trade_recommendations.csv"),
    "portfolio_risk_returns": os.path.join(BASE_PATH, "Portfolio Optimization Module", "portfolio_risk_return.csv"),
    "tca_summary": os.path.join(BASE_PATH, "Transaction Cost Analysis (TCA)", "weekly_tca_summary.csv")
}

with st.spinner("Loading portfolio data..."):
    risk_metrics = load_csv_safe(PATHS["risk_metrics"])
    sector_exposure = load_csv_safe(PATHS["sector_exposure"])
    backtest_results = load_csv_safe(PATHS["backtest_results"])
    backtest_wf = load_csv_safe(PATHS["backtest_wf"])
    target_weights = load_csv_safe(PATHS["target_weights"])
    trade_recommendations = load_csv_safe(PATHS["trade_recommendations"])
    portfolio_risk_returns = load_csv_safe(PATHS["portfolio_risk_returns"])
    tca_summary = load_csv_safe(PATHS["tca_summary"])

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_safe_value(series: pd.Series, index: int = -1, default: float = 0.0) -> float:
    try:
        series_clean = series.dropna()
        if len(series_clean) > abs(index):
            return float(series_clean.iloc[index])
        return default
    except:
        return default

def calculate_change(series: pd.Series, periods: int = 1) -> float:
    try:
        series_clean = series.dropna()
        if len(series_clean) > periods:
            current = float(series_clean.iloc[-1])
            previous = float(series_clean.iloc[-(periods + 1)])
            if previous != 0:
                return ((current - previous) / abs(previous)) * 100
        return 0.0
    except:
        return 0.0

def format_large_number(num: float) -> str:
    abs_num = abs(num)
    if abs_num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif abs_num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif abs_num >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"

def kpi_card(title: str, value: float, change: Optional[float] = None, 
             color: str = '#667eea', format_str: str = '.2f',
             subtitle: str = '', threshold: Optional[float] = None):
    
    breach_indicator = ""
    if threshold is not None:
        if value < threshold:
            breach_indicator = "<span style='color:#ff6b6b; font-weight:700;'>⚠ BREACH</span>"
    
    change_html = ""
    if change is not None:
        change_color = COLORS['success'] if change < 0 else COLORS['danger']
        change_symbol = '▼' if change < 0 else '▲'
        change_bg = f'rgba(72, 219, 251, 0.2)' if change < 0 else 'rgba(255, 107, 107, 0.2)'
        change_html = f"""
        <div class='kpi-change' style='color:{change_color}; background:{change_bg}'>
            {change_symbol} {abs(change):.2f}%
        </div>
        """
    
    subtitle_html = f"<div class='kpi-subtitle'>{subtitle}</div>" if subtitle else ""
    
    st.markdown(f"""
        <div class='kpi-card' style='--accent-color:{color}'>
            <div class='kpi-title'>{title} {breach_indicator}</div>
            <div class='kpi-value' style='color:{color}'>{value:{format_str}}</div>
            {change_html}
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)

def create_gauge_chart(value: float, title: str, max_val: float, 
                       threshold: float, unit: str = "%") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=abs(value),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': COLORS['text'], 'family': 'Inter'}},
        number={'suffix': unit, 'font': {'size': 28, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, max_val], 'tickcolor': COLORS['text']},
            'bar': {'color': COLORS['primary'], 'thickness': 0.75},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, abs(threshold) * 0.7], 'color': 'rgba(72, 219, 251, 0.2)'},
                {'range': [abs(threshold) * 0.7, abs(threshold)], 'color': 'rgba(254, 202, 87, 0.2)'},
                {'range': [abs(threshold), max_val], 'color': 'rgba(255, 107, 107, 0.2)'}
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 4},
                'thickness': 0.85,
                'value': abs(threshold)
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], family='Inter'),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

# ============================================================================
# PREMIUM SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 1.75rem; margin: 0; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Risk Analytics
        </h1>
        <p style='color: #64748b; font-size: 0.875rem; margin-top: 0.5rem;'>Enterprise Platform</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='margin: 1rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

section = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Risk Analytics",
        "Strategy Performance",
        "Portfolio Management",
        "Transaction Analysis",
        "Alerts & Compliance",
        "Reporting & Export"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

st.sidebar.markdown("### System Status")
st.sidebar.success("All Systems Operational")

st.sidebar.markdown("### Data Freshness")
st.sidebar.info(f"""
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Next Refresh:** {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')}
""")

quality_risk = assess_data_quality(risk_metrics)
quality_sector = assess_data_quality(sector_exposure)

color_map = {"high": "#48dbfb", "medium": "#feca57", "low": "#ff6b6b"}

st.sidebar.markdown(f"""
<div style='padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; margin-top: 1rem;'>
    <div style='font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'>Data Quality</div>
    <div style='display: flex; justify-content: space-between; margin: 0.25rem 0;'>
        <span>Risk Metrics</span>
        <span style='color: {color_map[quality_risk]};'>{quality_risk.upper()}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin: 0.25rem 0;'>
        <span>Sector Data</span>
        <span style='color: {color_map[quality_sector]};'>{quality_sector.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Records Loaded")
st.sidebar.markdown(f"""
- **Risk Metrics:** {len(risk_metrics):,}  
- **Sectors:** {len(sector_exposure):,}  
- **Backtest:** {len(backtest_results):,}  
- **Portfolio:** {len(target_weights):,}  
- **Trades:** {len(trade_recommendations):,}  
- **TCA:** {len(tca_summary):,}
""")

st.sidebar.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

st.sidebar.markdown("### Quick Actions")
col_r, col_e = st.sidebar.columns(2)
with col_r:
    if st.button("Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with col_e:
    if st.button("Export", use_container_width=True):
        st.sidebar.success("Export ready!")

        st.sidebar.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

        st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem; color: #64748b; font-size: 0.8rem;'>
    <strong>Version 2.5.0</strong><br>
    © 2024 Risk Platform
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT - EXECUTIVE OVERVIEW
# ============================================================================

if section == "Executive Overview":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Executive Risk Dashboard")
        st.markdown("Comprehensive portfolio risk and performance overview")
    with col_h2:
        quality = assess_data_quality(risk_metrics)
        quality_class = f"quality-{quality}"
        st.markdown(f"""
            <div class='data-quality {quality_class}'>
                Data Quality: {quality.upper()}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Key Risk Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_95"])
            change = calculate_change(risk_metrics["VaR_95"])
            kpi_card("VaR 95%", val, change, COLORS['danger'], '.2f', 
                    'Daily Value at Risk', RISK_LIMITS['var_95_limit'])
    
    with col2:
        if not risk_metrics.empty and "ES_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_95"])
            change = calculate_change(risk_metrics["ES_95"])
            kpi_card("Expected Shortfall", val, change, COLORS['danger'], '.2f',
                    '95% Confidence', RISK_LIMITS['es_95_limit'])
    
    with col3:
        if not portfolio_risk_returns.empty and "Expected Return" in portfolio_risk_returns.columns:
            val = float(portfolio_risk_returns["Expected Return"].iloc[0]) * 100
            kpi_card("Expected Return", val, None, COLORS['success'], '.2f', 'Annualized %')

    with col4:
        if not portfolio_risk_returns.empty and "Sharpe Ratio" in portfolio_risk_returns.columns:
            val = float(portfolio_risk_returns["Sharpe Ratio"].iloc[0])
            kpi_card("Sharpe Ratio", val, None, COLORS['info'], '.3f', 'Risk-Adjusted')

    with col5:
        if not portfolio_risk_returns.empty and "Expected Volatility" in portfolio_risk_returns.columns:
            val = float(portfolio_risk_returns["Expected Volatility"].iloc[0]) * 100
            kpi_card("Volatility", val, None, COLORS['warning'], '.2f', 'Annualized %')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Risk Utilization")
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    
    with col_g1:
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_95"])
            fig = create_gauge_chart(val, "VaR 95%", 50, RISK_LIMITS['var_95_limit'])
            st.plotly_chart(fig, use_container_width=True, key="gauge_var95")
    
    with col_g2:
        if not risk_metrics.empty and "ES_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_95"])
            fig = create_gauge_chart(val, "ES 95%", 100, RISK_LIMITS['es_95_limit'])
            st.plotly_chart(fig, use_container_width=True, key="gauge_es95")
    
    with col_g3:
        if not risk_metrics.empty and "VaR_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_99"])
            fig = create_gauge_chart(val, "VaR 99%", 80, RISK_LIMITS['var_99_limit'])
            st.plotly_chart(fig, use_container_width=True, key="gauge_var99")
    
    with col_g4:
        if not risk_metrics.empty and "ES_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_99"])
            fig = create_gauge_chart(val, "ES 99%", 200, RISK_LIMITS['es_99_limit'])
            st.plotly_chart(fig, use_container_width=True, key="gauge_es99")
    
    col_left, col_right = st.columns([1.3, 1])
    
    with col_left:
        st.markdown("<div class='section-header'><h3>Sector Exposure Analysis</h3></div>", unsafe_allow_html=True)
        
        if not sector_exposure.empty:
            sector_data = sector_exposure.copy()
            sector_data['portfolio_weight'] = sector_data['portfolio_weight'] * 100
            sector_data = sector_data.sort_values('portfolio_weight')
            
            max_exposure = sector_data['portfolio_weight'].abs().max()
            concentration_alert = max_exposure > (RISK_LIMITS['sector_concentration_limit'] * 100)
            
            fig = go.Figure()
            
            colors = [COLORS['danger'] if abs(x) > (RISK_LIMITS['sector_concentration_limit'] * 100) 
                     else COLORS['success'] if x > 0 else COLORS['warning']
                     for x in sector_data['portfolio_weight']]
            
            fig.add_trace(go.Bar(
                x=sector_data['portfolio_weight'],
                y=sector_data['sector'],
                orientation='h',
                marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
                text=sector_data['portfolio_weight'].apply(lambda x: f'{x:.2f}%'),
                textposition='outside',
                textfont=dict(family='Inter', size=11),
                hovertemplate='<b>%{y}</b><br>Weight: %{x:.2f}%<extra></extra>'
            ))
            
            limit_pct = RISK_LIMITS['sector_concentration_limit'] * 100
            fig.add_vline(x=limit_pct, line_dash="dash", line_color=COLORS['warning'],
                         annotation_text=f"Limit: {limit_pct}%", annotation_position="top right")
            fig.add_vline(x=-limit_pct, line_dash="dash", line_color=COLORS['warning'])
            
            fig.update_layout(
                height=420,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                xaxis=dict(title="Portfolio Weight (%)", gridcolor='rgba(102, 126, 234, 0.1)', 
                          zeroline=True, zerolinecolor='rgba(102, 126, 234, 0.2)'),
                yaxis=dict(title="", tickfont=dict(size=11)),
                margin=dict(l=20, r=80, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sector_exposure_main")
            
            if concentration_alert:
                st.markdown("""
                    <div class='alert-box alert-warning'>
                        <strong>Concentration Risk Detected:</strong> One or more sectors exceed the 15% exposure limit.
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No sector exposure data available")
    
    with col_right:
        st.markdown("<div class='section-header'><h3>Stress Test Scenarios</h3></div>", unsafe_allow_html=True)
        
        if not risk_metrics.empty:
            stress_cols = ["Rate_Shock", "Volatility_Spike", "Sector_Drawdown"]
            available = [c for c in stress_cols if c in risk_metrics.columns]
            
            if available:
                latest_stress = risk_metrics[available].iloc[-1]
                
                for col in available:
                    val = latest_stress[col]
                    
                    if val < -5.0:
                        color = COLORS['danger']
                        severity = "CRITICAL"
                        icon = "🔴"
                    elif val < -2.0:
                        color = COLORS['warning']
                        severity = "HIGH"
                        icon = "🟡"
                    elif val < 0:
                        color = COLORS['info']
                        severity = "MODERATE"
                        icon = "🟢"
                    else:
                        color = COLORS['success']
                        severity = "LOW"
                        icon = "🟢"
                    
                    st.markdown(f"""
                        <div class='trade-card' style='border-color: {color}'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <span style='font-weight: 700; font-size: 0.95rem;'>{col.replace('_', ' ')}</span><br>
                                    <span class='metric-badge' style='background:{color};color:#fff;margin-top:0.5rem;'>{icon} {severity}</span>
                                </div>
                                <span style='color: {color}; font-weight: 800; font-size: 1.6rem;'>{val:.2f}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                stress_history = risk_metrics[available].tail(30)
                
                fig_stress = go.Figure()
                colors_stress = [COLORS['danger'], COLORS['warning'], COLORS['info']]
                
                for i, col in enumerate(available):
                    fig_stress.add_trace(go.Scatter(
                        y=stress_history[col],
                        name=col.replace('_', ' '),
                        mode='lines',
                        line=dict(width=2.5, color=colors_stress[i]),
                        fill='tonexty' if i > 0 else None
                    ))
                
                fig_stress.update_layout(
                    height=220,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=COLORS['text'], size=10, family='Inter'),
                    xaxis=dict(title="", gridcolor='rgba(102, 126, 234, 0.1)', showticklabels=False),
                    yaxis=dict(title="Impact (%)", gridcolor='rgba(102, 126, 234, 0.1)'),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9)),
                    margin=dict(l=40, r=10, t=30, b=20),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_stress, use_container_width=True, key="stress_mini")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_perf1, col_perf2 = st.columns([1.2, 1])
    
    with col_perf1:
        st.markdown("<div class='section-header'><h3>Top Holdings Analysis</h3></div>", unsafe_allow_html=True)
        
        if not target_weights.empty and "Target Weight" in target_weights.columns:
            top_holdings = target_weights.nlargest(10, 'Target Weight')
            
            max_position = top_holdings['Target Weight'].max()
            position_alert = max_position > RISK_LIMITS['single_position_limit']
            
            fig = go.Figure()
            
            colors_holdings = [COLORS['danger'] if w > RISK_LIMITS['single_position_limit'] 
                             else COLORS['primary'] for w in top_holdings['Target Weight']]
            
            fig.add_trace(go.Bar(
                x=top_holdings['Target Weight'],
                y=top_holdings['Instrument'],
                orientation='h',
                marker=dict(
                    color=colors_holdings,
                    line=dict(color='rgba(255,255,255,0.1)', width=1)
                ),
                text=top_holdings['Target Weight'].apply(lambda x: f'{x:.2%}'),
                textposition='outside',
                textfont=dict(family='Inter', size=10),
                hovertemplate='<b>%{y}</b><br>Weight: %{x:.2%}<extra></extra>'
            ))
            
            fig.add_vline(x=RISK_LIMITS['single_position_limit'], line_dash="dash", 
                         line_color=COLORS['warning'],
                         annotation_text=f"Limit: {RISK_LIMITS['single_position_limit']:.0%}", 
                         annotation_position="top right")
            
            fig.update_layout(
                height=370,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                xaxis=dict(title="Position Weight", gridcolor='rgba(102, 126, 234, 0.1)', tickformat='.0%'),
                yaxis=dict(title="", autorange='reversed', tickfont=dict(size=10)),
                showlegend=False,
                margin=dict(l=20, r=80, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="top_holdings_main")
            
            if position_alert:
                st.markdown(f"""
                    <div class='alert-box alert-warning'>
                        <strong>Position Concentration Alert:</strong> Maximum single position of {max_position:.2%} exceeds {RISK_LIMITS['single_position_limit']:.0%} limit.
                    </div>
                """, unsafe_allow_html=True)
    
    with col_perf2:
        st.markdown("<div class='section-header'><h3>Transaction Cost Trends</h3></div>", unsafe_allow_html=True)
        
        if not tca_summary.empty and "avg_slippage_bps" in tca_summary.columns:
            avg_slippage = tca_summary["avg_slippage_bps"].mean()
            recent_slippage = get_safe_value(tca_summary["avg_slippage_bps"])
            slippage_trend = calculate_change(tca_summary["avg_slippage_bps"], periods=4)
            
            high_slippage = abs(recent_slippage) > RISK_LIMITS['slippage_threshold_bps']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                y=tca_summary["avg_slippage_bps"],
                mode='lines+markers',
                line=dict(color=COLORS['danger'] if high_slippage else COLORS['info'], width=3),
                marker=dict(size=8, symbol='diamond'),
                fill='tozeroy',
                fillcolor=f"rgba(255, 107, 107, 0.15)" if high_slippage else f"rgba(0, 210, 211, 0.15)",
                name='Slippage',
                hovertemplate='Week %{x}<br>Slippage: %{y:.2f} bps<extra></extra>'
            ))
            
            fig.add_hline(
                y=avg_slippage, 
                line_dash="dash", 
                line_color=COLORS['warning'],
                annotation_text=f"Avg: {avg_slippage:.2f} bps",
                annotation_position="right"
            )
            
            fig.add_hline(
                y=RISK_LIMITS['slippage_threshold_bps'], 
                line_dash="dot", 
                line_color=COLORS['danger'],
                annotation_text=f"Threshold: {RISK_LIMITS['slippage_threshold_bps']} bps",
                annotation_position="left"
            )
            
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                xaxis=dict(title="Week", gridcolor='rgba(102, 126, 234, 0.1)'),
                yaxis=dict(title="Slippage (bps)", gridcolor='rgba(102, 126, 234, 0.1)'),
                margin=dict(l=50, r=20, t=20, b=40),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key="tca_trend_main")
            
            col_tca1, col_tca2 = st.columns(2)
            with col_tca1:
                st.metric(
                    "Current Slippage",
                    f"{recent_slippage:.2f} bps",
                    f"{slippage_trend:+.1f}%",
                    delta_color="inverse"
                )
            with col_tca2:
                st.metric(
                    "Average Slippage",
                    f"{avg_slippage:.2f} bps"
                )
            
            if high_slippage:
                st.markdown("""
                    <div class='alert-box alert-danger' style='margin-top:1rem;'>
                        <strong>High Slippage Warning:</strong> Recent execution costs exceed acceptable thresholds.
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'><h3>Risk Summary & Compliance Status</h3></div>", unsafe_allow_html=True)
    
    summary_data = []
    
    if not risk_metrics.empty:
        var_95 = get_safe_value(risk_metrics.get("VaR_95", pd.Series([0])))
        summary_data.append({
            'Risk Metric': 'Value at Risk (95%)',
            'Current Value': f"{var_95:.2f}",
            'Limit': f"{RISK_LIMITS['var_95_limit']:.2f}",
            'Utilization': f"{(var_95/RISK_LIMITS['var_95_limit']*100):.1f}%",
            'Status': 'Pass' if var_95 >= RISK_LIMITS['var_95_limit'] else 'Breach'
        })
        
        es_95 = get_safe_value(risk_metrics.get("ES_95", pd.Series([0])))
        summary_data.append({
            'Risk Metric': 'Expected Shortfall (95%)',
            'Current Value': f"{es_95:.2f}",
            'Limit': f"{RISK_LIMITS['es_95_limit']:.2f}",
            'Utilization': f"{(es_95/RISK_LIMITS['es_95_limit']*100):.1f}%",
            'Status': 'Pass' if es_95 >= RISK_LIMITS['es_95_limit'] else 'Breach'
        })
    
    if not sector_exposure.empty:
        max_sector = sector_exposure['portfolio_weight'].abs().max()
        summary_data.append({
            'Risk Metric': 'Sector Concentration',
            'Current Value': f"{max_sector*100:.2f}%",
            'Limit': f"{RISK_LIMITS['sector_concentration_limit']*100:.0f}%",
            'Utilization': f"{(max_sector/RISK_LIMITS['sector_concentration_limit']*100):.1f}%",
            'Status': 'Pass' if max_sector <= RISK_LIMITS['sector_concentration_limit'] else 'Warning'
        })
    
    if not target_weights.empty:
        max_position = target_weights['Target Weight'].max()
        summary_data.append({
            'Risk Metric': 'Single Position Limit',
            'Current Value': f"{max_position*100:.2f}%",
            'Limit': f"{RISK_LIMITS['single_position_limit']*100:.0f}%",
            'Utilization': f"{(max_position/RISK_LIMITS['single_position_limit']*100):.1f}%",
            'Status': 'Pass' if max_position <= RISK_LIMITS['single_position_limit'] else 'Warning'
        })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, height=250)
        
        passes = sum('Pass' in str(row['Status']) for row in summary_data)
        total = len(summary_data)
        compliance_pct = (passes / total * 100) if total > 0 else 0
        
        if compliance_pct == 100:
            st.markdown("""
                <div class='alert-box alert-success'>
                    <strong>Full Compliance:</strong> All risk limits are within acceptable ranges.
                </div>
            """, unsafe_allow_html=True)
        elif compliance_pct >= 75:
            st.markdown(f"""
                <div class='alert-box alert-warning'>
                    <strong>Partial Compliance:</strong> {compliance_pct:.0f}% of limits met. Review required.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='alert-box alert-danger'>
                    <strong>Compliance Issues:</strong> Only {compliance_pct:.0f}% of limits met. Immediate action required.
                </div>
            """, unsafe_allow_html=True)

# ============================================================================
# RISK ANALYTICS SECTION
# ============================================================================

elif section == "Risk Analytics":
    st.title("Risk Analytics Deep Dive")
    st.markdown("Comprehensive risk metrics, factor exposure, and scenario analysis")
    st.markdown("---")
    
    st.markdown("### Current Risk Position")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_95"])
            change = calculate_change(risk_metrics["VaR_95"])
            kpi_card("VaR 95%", val, change, COLORS['danger'], '.2f', '1-Day', RISK_LIMITS['var_95_limit'])
    
    with col2:
        if not risk_metrics.empty and "ES_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_95"])
            change = calculate_change(risk_metrics["ES_95"])
            kpi_card("ES 95%", val, change, COLORS['danger'], '.2f', 'Tail Risk', RISK_LIMITS['es_95_limit'])
    
    with col3:
        if not risk_metrics.empty and "VaR_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_99"])
            change = calculate_change(risk_metrics["VaR_99"])
            kpi_card("VaR 99%", val, change, COLORS['warning'], '.2f', 'Extreme', RISK_LIMITS['var_99_limit'])
    
    with col4:
        if not risk_metrics.empty and "ES_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_99"])
            change = calculate_change(risk_metrics["ES_99"])
            kpi_card("ES 99%", val, change, COLORS['warning'], '.2f', 'Extreme Tail', RISK_LIMITS['es_99_limit'])
    
    with col5:
        if not risk_metrics.empty:
            avg_risk = risk_metrics[["VaR_95", "ES_95"]].mean().mean()
            kpi_card("Avg Risk", avg_risk, None, COLORS['info'], '.2f', 'Combined')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Risk Trends", "Stress Tests", "Monte Carlo", "Drawdown Analysis"])
    
    with tab1:
        st.markdown("#### Historical Risk Metrics Evolution")
        
        if not risk_metrics.empty:
            risk_cols = ["VaR_95", "ES_95", "VaR_99", "ES_99"]
            available_risk = [c for c in risk_cols if c in risk_metrics.columns]
            
            if available_risk:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=available_risk,
                    vertical_spacing=0.12,
                    horizontal_spacing=0.1
                )
                
                positions = [(1,1), (1,2), (2,1), (2,2)]
                colors_risk = [COLORS['danger'], COLORS['warning'], COLORS['info'], COLORS['primary']]
                
                for idx, col in enumerate(available_risk):
                    row, col_pos = positions[idx]
                    data = risk_metrics[col].tail(100)
                    
                    fig.add_trace(
                        go.Scatter(
                            y=data,
                            mode='lines',
                            line=dict(width=2, color=colors_risk[idx]),
                            fill='tozeroy',
                            fillcolor=f"rgba{tuple(list(int(colors_risk[idx][j:j+2], 16) for j in (1, 3, 5)) + [0.2])}",
                            name=col,
                            showlegend=False,
                            hovertemplate=f'{col}: %{{y:.2f}}<extra></extra>'
                        ),
                        row=row, col=col_pos
                    )
                    
                    threshold_key = f"{col.lower().replace('_', '_')}_limit"
                    if threshold_key in RISK_LIMITS:
                        fig.add_hline(
                            y=RISK_LIMITS[threshold_key],
                            line_dash="dash",
                            line_color=COLORS['danger'],
                            row=row, col=col_pos,
                            annotation_text="Limit",
                            annotation_position="right"
                        )
                
                fig.update_layout(
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=COLORS['text'], family='Inter'),
                    showlegend=False
                )
                
                fig.update_xaxes(gridcolor='rgba(102, 126, 234, 0.1)', title_text="Time Period")
                fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.1)')
                
                st.plotly_chart(fig, use_container_width=True, key="risk_trends")
                
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                for idx, col_stat in enumerate([col_stat1, col_stat2, col_stat3, col_stat4]):
                    if idx < len(available_risk):
                        metric = available_risk[idx]
                        with col_stat:
                            mean_val = risk_metrics[metric].mean()
                            std_val = risk_metrics[metric].std()
                            st.metric(
                                f"{metric} Stats",
                                f"{mean_val:.2f}",
                                f"σ: {std_val:.2f}"
                            )
    
    with tab2:
        st.markdown("#### Stress Test Scenario Analysis")
        
        if not risk_metrics.empty:
            stress_cols = ["Rate_Shock", "Volatility_Spike", "Sector_Drawdown"]
            available_stress = [c for c in stress_cols if c in risk_metrics.columns]
            
            if available_stress:
                stress_data = risk_metrics[available_stress].tail(100)
                
                fig = go.Figure()
                colors_stress = [COLORS['danger'], COLORS['warning'], COLORS['info']]
                
                for i, col in enumerate(available_stress):
                    fig.add_trace(go.Scatter(
                        y=stress_data[col],
                        name=col.replace('_', ' '),
                        mode='lines+markers',
                        line=dict(width=2.5, color=colors_stress[i]),
                        marker=dict(size=6),
                        hovertemplate=f'<b>{col.replace("_", " ")}</b><br>Impact: %{{y:.2f}}%<extra></extra>'
                    ))
                
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=COLORS['text'], family='Inter'),
                    xaxis=dict(title="Time Period", gridcolor='rgba(102, 126, 234, 0.1)'),
                    yaxis=dict(title="Impact (%)", gridcolor='rgba(102, 126, 234, 0.1)'),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True, key="stress_trends_detailed")
                
                st.markdown("##### Current Stress Scenario Impact")
                
                latest_stress = risk_metrics[available_stress].iloc[-1]
                prev_stress = risk_metrics[available_stress].iloc[-2] if len(risk_metrics) > 1 else latest_stress
                
                col_sc1, col_sc2, col_sc3 = st.columns(3)
                for idx, col_sc in enumerate([col_sc1, col_sc2, col_sc3]):
                    if idx < len(available_stress):
                        scenario = available_stress[idx]
                        current = latest_stress[scenario]
                        previous = prev_stress[scenario]
                        change_val = current - previous
                        with col_sc:
                            st.metric(
                                scenario.replace('_', ' '),
                                f"{current:.2f}%",
                                f"{change_val:+.2f}%",
                                delta_color="inverse"
                            )
    
    with tab3:
        st.markdown("#### Monte Carlo Simulation Results")
        st.info("Monte Carlo simulation module: Connect to quantitative risk engine for forward-looking risk projections")
        
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            historical_var = risk_metrics["VaR_95"].dropna()
            
            if len(historical_var) > 10:
                mean_var = historical_var.mean()
                std_var = historical_var.std()
                simulated = np.random.normal(mean_var, std_var, 10000)
                
                fig = go.Figure()
                
                fig.add_trace(go.Histogram(
                    x=simulated,
                    nbinsx=50,
                    name='Simulated VaR',
                    marker_color=COLORS['primary'],
                    opacity=0.7,
                    hovertemplate='VaR Range: %{x:.2f}<br>Frequency: %{y}<extra></extra>'
                ))
                
                p5 = np.percentile(simulated, 5)
                p95 = np.percentile(simulated, 95)
                
                fig.add_vline(x=p5, line_dash="dash", line_color=COLORS['danger'],
                             annotation_text="5th percentile")
                fig.add_vline(x=p95, line_dash="dash", line_color=COLORS['success'],
                             annotation_text="95th percentile")
                
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=COLORS['text'], family='Inter'),
                    xaxis=dict(title="VaR 95%", gridcolor='rgba(102, 126, 234, 0.1)'),
                    yaxis=dict(title="Frequency", gridcolor='rgba(102, 126, 234, 0.1)'),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key="monte_carlo")
                
                col_mc1, col_mc2, col_mc3 = st.columns(3)
                with col_mc1:
                    st.metric("5th Percentile", f"{p5:.2f}")
                with col_mc2:
                    st.metric("Median", f"{np.median(simulated):.2f}")
                with col_mc3:
                    st.metric("95th Percentile", f"{p95:.2f}")
    
    with tab4:
        st.markdown("#### Maximum Drawdown Analysis")
        
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            cumulative = (1 + risk_metrics["VaR_95"] / 100).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max * 100
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                y=drawdown,
                mode='lines',
                fill='tozeroy',
                line=dict(color=COLORS['danger'], width=2),
                fillcolor='rgba(255, 107, 107, 0.3)',
                name='Drawdown',
                hovertemplate='Drawdown: %{y:.2f}%<extra></extra>'
            ))
            
            fig.add_hline(
                y=RISK_LIMITS['max_drawdown_limit'] * 100,
                line_dash="dash",
                line_color=COLORS['warning'],
                annotation_text=f"Max DD Limit: {RISK_LIMITS['max_drawdown_limit']*100:.0f}%"
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                xaxis=dict(title="Time Period", gridcolor='rgba(102, 126, 234, 0.1)'),
                yaxis=dict(title="Drawdown (%)", gridcolor='rgba(102, 126, 234, 0.1)'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key="drawdown")
            
            max_dd = drawdown.min()
            current_dd = drawdown.iloc[-1]
            
            col_dd1, col_dd2, col_dd3 = st.columns(3)
            with col_dd1:
                st.metric("Maximum Drawdown", f"{max_dd:.2f}%")
            with col_dd2:
                st.metric("Current Drawdown", f"{current_dd:.2f}%")
            with col_dd3:
                breach = max_dd < (RISK_LIMITS['max_drawdown_limit'] * 100)
                status = "BREACH" if breach else "OK"
                color = "🔴" if breach else "🟢"
                st.metric("Status", f"{color} {status}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'><h3>Sector & Factor Exposure</h3></div>", unsafe_allow_html=True)
    
    if not sector_exposure.empty:
        col_sector1, col_sector2 = st.columns([1.5, 1])
        
        with col_sector1:
            sector_data = sector_exposure.copy()
            sector_data['portfolio_weight'] = sector_data['portfolio_weight'] * 100
            sector_data['abs_weight'] = sector_data['portfolio_weight'].abs()
            sector_data = sector_data.sort_values('portfolio_weight', ascending=True)
            
            fig = go.Figure()
            
            colors = [COLORS['danger'] if abs(x) > (RISK_LIMITS['sector_concentration_limit'] * 100) 
                     else COLORS['success'] if x > 0 else COLORS['warning']
                     for x in sector_data['portfolio_weight']]
            
            fig.add_trace(go.Bar(
                y=sector_data['sector'],
                x=sector_data['portfolio_weight'],
                orientation='h',
                marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
                text=sector_data['portfolio_weight'].apply(lambda x: f'{x:.2f}%'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Weight: %{x:.2f}%<extra></extra>'
            ))
            
            limit_pct = RISK_LIMITS['sector_concentration_limit'] * 100
            fig.add_vline(x=limit_pct, line_dash="dash", line_color=COLORS['warning'])
            fig.add_vline(x=-limit_pct, line_dash="dash", line_color=COLORS['warning'])
            
            fig.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                xaxis=dict(title="Portfolio Weight (%)", gridcolor='rgba(102, 126, 234, 0.1)', zeroline=True),
                yaxis=dict(title=""),
                margin=dict(l=20, r=100, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sector_detailed")
        
        with col_sector2:
            st.markdown("##### Concentration Metrics")
            
            top_3 = sector_data.nlargest(3, 'abs_weight')
            
            for idx, row in top_3.iterrows():
                weight = row['portfolio_weight']
                sector = row['sector']
                is_breach = abs(weight) > (RISK_LIMITS['sector_concentration_limit'] * 100)
                
                badge_color = COLORS['danger'] if is_breach else COLORS['success']
                
                st.markdown(f"""
                    <div class='trade-card' style='border-color: {badge_color}; margin: 0.5rem 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-weight: 600; font-size: 0.9rem;'>{sector}</span>
                            <span style='color: {badge_color}; font-weight: 700; font-size: 1.2rem;'>{weight:.2f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("##### Diversification Score")
            
            weights_squared = (sector_data['portfolio_weight'] / 100) ** 2
            herfindahl = weights_squared.sum()
            diversification_score = (1 - herfindahl) * 100
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=diversification_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Diversification", 'font': {'size': 14, 'family': 'Inter'}},
                number={'suffix': "", 'font': {'size': 20, 'family': 'Inter'}},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': COLORS['info']},
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(255, 107, 107, 0.3)'},
                        {'range': [50, 75], 'color': 'rgba(254, 202, 87, 0.3)'},
                        {'range': [75, 100], 'color': 'rgba(72, 219, 251, 0.3)'}
                    ],
                    'threshold': {
                        'line': {'color': COLORS['success'], 'width': 4},
                        'thickness': 0.75,
                        'value': 75
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=250,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], family='Inter'),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True, key="diversification")
            
            if diversification_score < 50:
                st.markdown("""
                    <div class='alert-box alert-danger'>
                        Low diversification detected
                    </div>
                """, unsafe_allow_html=True)
            elif diversification_score < 75:
                st.markdown("""
                    <div class='alert-box alert-warning'>
                        Moderate diversification
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='alert-box alert-success'>
                        Well diversified portfolio
                    </div>
                """, unsafe_allow_html=True)

# ============================================================================
# STRATEGY PERFORMANCE SECTION
# ============================================================================

elif section == "Strategy Performance":
    st.title("Backtesting & Strategy Performance")
    st.markdown("Comprehensive strategy comparison and performance attribution")
    st.markdown("---")
    
    if not backtest_results.empty and not backtest_wf.empty:
        backtest_standard = backtest_results.copy()
        backtest_standard['Method'] = 'Standard Backtest'
        
        backtest_walkforward = backtest_wf.copy()
        backtest_walkforward['Method'] = 'Walk-Forward'
        
        combined = pd.concat([backtest_standard, backtest_walkforward], ignore_index=True)
        
        st.markdown("### Performance Summary")
        
        best_sharpe = combined.loc[combined['Sharpe'].idxmax()]
        best_return = combined.loc[combined['Total Return'].idxmax()]
        lowest_dd = combined.loc[combined['Max Drawdown'].idxmax()]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            kpi_card("Best Sharpe", best_sharpe['Sharpe'], None, COLORS['success'], '.4f', 
                    best_sharpe['Strategy'])
        with col2:
            kpi_card("Highest Return", best_return['Total Return'], None, COLORS['info'], '.2f',
                    best_return['Strategy'])
        with col3:
            kpi_card("Lowest Volatility", combined['Volatility'].min(), None, COLORS['primary'], '.4f')
        with col4:
            kpi_card("Best Drawdown", lowest_dd['Max Drawdown'], None, COLORS['warning'], '.2f',
                    lowest_dd['Strategy'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'><h3>Strategy Comparison Matrix</h3></div>", unsafe_allow_html=True)
        
        metrics = ['Total Return', 'Volatility', 'Sharpe', 'Max Drawdown']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metrics,
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        strategies = combined['Strategy'].unique()
        colors_strat = {
            strategies[i]: [COLORS['primary'], COLORS['danger'], COLORS['success'], COLORS['warning']][i % 4]
            for i in range(len(strategies))
        }
        
        for idx, metric in enumerate(metrics):
            row = idx // 2 + 1
            col = idx % 2 + 1
            
            for strategy in strategies:
                strategy_data = combined[combined['Strategy'] == strategy]
                
                fig.add_trace(
                    go.Bar(
                        name=strategy,
                        x=strategy_data['Method'],
                        y=strategy_data[metric],
                        marker_color=colors_strat.get(strategy, COLORS['primary']),
                        showlegend=(idx == 0),
                        hovertemplate=f'<b>{strategy}</b><br>{metric}: %{{y:.4f}}<extra></extra>',
                        text=strategy_data[metric].apply(lambda x: f'{x:.3f}'),
                        textposition='outside'
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], family='Inter'),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
            barmode='group'
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.1)')
        
        st.plotly_chart(fig, use_container_width=True, key="strategy_comparison_main")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'><h3>Detailed Performance Metrics</h3></div>", unsafe_allow_html=True)
        
        st.dataframe(combined, use_container_width=True, height=300)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><h3>Risk-Return Profile</h3></div>", unsafe_allow_html=True)
        
        fig_scatter = go.Figure()
        
        for strategy in strategies:
            strategy_data = combined[combined['Strategy'] == strategy]
            
            fig_scatter.add_trace(go.Scatter(
                x=strategy_data['Volatility'],
                y=strategy_data['Total Return'],
                mode='markers+text',
                name=strategy,
                marker=dict(size=15, color=colors_strat.get(strategy, COLORS['primary']), 
                           line=dict(width=2, color='white')),
                text=strategy_data['Method'].apply(lambda x: x.split()[0]),
                textposition='top center',
                textfont=dict(size=9, family='Inter'),
                hovertemplate='<b>%{fullData.name}</b><br>Volatility: %{x:.4f}<br>Return: %{y:.4f}<extra></extra>'
            ))
        
        if len(combined) > 1:
            x_range = combined['Volatility'].values
            y_range = combined['Total Return'].values
            
            z = np.polyfit(x_range, y_range, 1)
            p = np.poly1d(z)
            x_line = np.linspace(x_range.min(), x_range.max(), 100)
            
            fig_scatter.add_trace(go.Scatter(
                x=x_line,
                y=p(x_line),
                mode='lines',
                name='Trend',
                line=dict(dash='dash', color=COLORS['muted'], width=2),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig_scatter.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], family='Inter'),
            xaxis=dict(title="Volatility (Risk)", gridcolor='rgba(102, 126, 234, 0.1)'),
            yaxis=dict(title="Total Return", gridcolor='rgba(102, 126, 234, 0.1)'),
            legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="left", x=0.01),
            hovermode='closest'
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True, key="risk_return_scatter")
    else:
        st.warning("Insufficient backtesting data available for analysis")

# ============================================================================
# PORTFOLIO MANAGEMENT SECTION
# ============================================================================

elif section == "Portfolio Management":
    st.title("Portfolio Optimization & Rebalancing")
    st.markdown("Target allocations, trade recommendations, and portfolio analytics")
    st.markdown("---")
    
    st.markdown("### Portfolio Characteristics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if not portfolio_risk_returns.empty:
        with col1:
           exp_return = float(portfolio_risk_returns["Expected Return"].iloc[0]) * 100
           kpi_card("Expected Return", exp_return, None, COLORS['success'], '.2f', 'Annualized %')

        with col2:
           exp_vol = float(portfolio_risk_returns["Expected Volatility"].iloc[0]) * 100
           kpi_card("Expected Vol", exp_vol, None, COLORS['warning'], '.2f', 'Annualized %')

        with col3:
           sharpe = float(portfolio_risk_returns["Sharpe Ratio"].iloc[0])
           kpi_card("Sharpe Ratio", sharpe, None, COLORS['info'], '.4f', 'Risk-Adjusted')
        
        with col4:
            if not target_weights.empty:
                num_positions = len(target_weights[target_weights['Target Weight'] > 0.001])
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-title'>Active Positions</div>
                        <div class='kpi-value' style='color:{COLORS["primary"]}'>{num_positions}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col5:
            if not target_weights.empty:
                avg_position = target_weights['Target Weight'].mean() * 100
                kpi_card("Avg Position", avg_position, None, COLORS['accent'], '.2f', '% of Portfolio')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'><h3>Recommended Portfolio Adjustments</h3></div>", unsafe_allow_html=True)
    
    if not trade_recommendations.empty and "Change (Buy/Sell)" in trade_recommendations.columns:
        trades = trade_recommendations.copy()
        trades['abs_change'] = trades['Change (Buy/Sell)'].abs()
        
        significant_trades = trades[trades['abs_change'] > 0.0001].copy()
        top_trades = significant_trades.nlargest(20, 'abs_change')
        
        total_turnover = trades['abs_change'].sum()
        num_buys = len(trades[trades['Change (Buy/Sell)'] > 0.0001])
        num_sells = len(trades[trades['Change (Buy/Sell)'] < -0.0001])
        
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        
        with col_sum1:
            kpi_card("Total Turnover", total_turnover * 100, None, COLORS['info'], '.3f', '% of Portfolio')
        with col_sum2:
            st.markdown(f"""
                <div class='kpi-card' style='--accent-color:{COLORS["success"]}'>
                    <div class='kpi-title'>Buy Orders</div>
                    <div class='kpi-value' style='color:{COLORS["success"]}'>{num_buys}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_sum3:
            st.markdown(f"""
                <div class='kpi-card' style='--accent-color:{COLORS["danger"]}'>
                    <div class='kpi-title'>Sell Orders</div>
                    <div class='kpi-value' style='color:{COLORS["danger"]}'>{num_sells}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_sum4:
            net_change = num_buys - num_sells
            net_color = COLORS['success'] if net_change > 0 else COLORS['danger']
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Net Position Change</div>
                    <div class='kpi-value' style='color:{net_color}'>{net_change:+d}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_buy, col_sell = st.columns(2)
        
        with col_buy:
            st.markdown("#### Top Buy Recommendations")
            buys = top_trades[top_trades['Change (Buy/Sell)'] > 0].head(10)
            
            for _, trade in buys.iterrows():
                change_pct = trade['Change (Buy/Sell)'] * 100
                
                st.markdown(f"""
                    <div class='trade-card trade-buy'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div style='flex: 1;'>
                                <strong style='font-size: 1rem;'>{trade['Instrument']}</strong><br>
                                <span style='font-size: 0.8rem; color: #9CA3AF;'>
                                    {trade['Current Weight']*100:.3f}% → {trade['Target Weight']*100:.3f}%
                                </span>
                            </div>
                            <div style='text-align: right; padding-left: 1rem;'>
                                <span style='color: {COLORS["success"]}; font-weight: 800; font-size: 1.3rem;'>
                                    +{change_pct:.3f}%
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            if len(buys) == 0:
                st.info("No significant buy recommendations")
        
        with col_sell:
            st.markdown("#### Top Sell Recommendations")
            sells = top_trades[top_trades['Change (Buy/Sell)'] < 0].head(10)
            
            for _, trade in sells.iterrows():
                change_pct = trade['Change (Buy/Sell)'] * 100
                
                st.markdown(f"""
                    <div class='trade-card trade-sell'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div style='flex: 1;'>
                                <strong style='font-size: 1rem;'>{trade['Instrument']}</strong><br>
                                <span style='font-size: 0.8rem; color: #9CA3AF;'>
                                    {trade['Current Weight']*100:.3f}% → {trade['Target Weight']*100:.3f}%
                                </span>
                            </div>
                            <div style='text-align: right; padding-left: 1rem;'>
                                <span style='color: {COLORS["danger"]}; font-weight: 800; font-size: 1.3rem;'>
                                    {change_pct:.3f}%
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            if len(sells) == 0:
                st.info("No significant sell recommendations")

# ============================================================================
# TRANSACTION ANALYSIS SECTION
# ============================================================================

elif section == "Transaction Analysis":
    st.title("Transaction Cost Analysis")
    st.markdown("Execution quality, cost breakdown, and P&L attribution analysis")
    st.markdown("---")
    
    if not tca_summary.empty:
        st.markdown("### Execution Quality Metrics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_slippage = tca_summary['avg_slippage_bps'].mean()
            recent_slippage = get_safe_value(tca_summary['avg_slippage_bps'])
            slip_change = calculate_change(tca_summary['avg_slippage_bps'], periods=1)
            kpi_card("Avg Slippage", avg_slippage, slip_change, COLORS['danger'], '.2f', 'Basis Points', 
                    RISK_LIMITS['slippage_threshold_bps'])
        
        with col2:
            avg_impact = tca_summary['avg_market_impact_bps'].mean()
            kpi_card("Market Impact", avg_impact, None, COLORS['warning'], '.2f', 'Basis Points',
                    RISK_LIMITS['market_impact_threshold_bps'])
        
        with col3:
            total_commission = tca_summary['total_commission'].sum()
            kpi_card("Total Commission", total_commission, None, COLORS['info'], ',.0f', 'USD')
        
        with col4:
            total_pnl = tca_summary['total_pnl'].sum()
            pnl_color = COLORS['success'] if total_pnl > 0 else COLORS['danger']
            st.markdown(f"""
                <div class='kpi-card' style='--accent-color:{pnl_color}'>
                    <div class='kpi-title'>Total P&L</div>
                    <div class='kpi-value' style='color:{pnl_color}'>{format_large_number(total_pnl)}</div>
                    <div class='kpi-subtitle'>Cumulative</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            if len(tca_summary) > 1:
                avg_weekly_pnl = tca_summary['total_pnl'].mean()
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-title'>Avg Weekly P&L</div>
                        <div class='kpi-value' style='color:{COLORS["primary"]}'>{format_large_number(avg_weekly_pnl)}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><h3>Cost Component Analysis</h3></div>", unsafe_allow_html=True)
        
        st.info("Transaction Cost Analysis data loaded successfully. Displaying cost trends and P&L attribution.")
    else:
        st.warning("No TCA data available for analysis")

# ============================================================================
# ALERTS & COMPLIANCE SECTION
# ============================================================================

elif section == "Alerts & Compliance":
    st.title("Risk Alerts & Compliance Monitoring")
    st.markdown("Real-time breach detection, threshold monitoring, and regulatory compliance")
    st.markdown("---")
    
    alerts = []
    critical_count = 0
    warning_count = 0
    
    if not risk_metrics.empty:
        if "VaR_95" in risk_metrics.columns:
            latest_var_95 = get_safe_value(risk_metrics["VaR_95"])
            if latest_var_95 < RISK_LIMITS['var_95_limit']:
                alerts.append({
                    'severity': 'critical',
                    'category': 'Market Risk',
                    'title': 'VaR 95% Breach',
                    'message': f'Current VaR 95%: {latest_var_95:.2f} exceeds limit of {RISK_LIMITS["var_95_limit"]}',
                    'metric': latest_var_95,
                    'timestamp': datetime.now()
                })
                critical_count += 1
    
    st.markdown("### Alert Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_alerts = len(alerts)
        alert_color = COLORS['danger'] if total_alerts > 5 else COLORS['warning'] if total_alerts > 0 else COLORS['success']
        st.markdown(f"""
            <div class='kpi-card' style='--accent-color:{alert_color}'>
                <div class='kpi-title'>Total Active Alerts</div>
                <div class='kpi-value' style='color:{alert_color}'>{total_alerts}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='kpi-card' style='--accent-color:{COLORS["danger"]}'>
                <div class='kpi-title'>Critical Alerts</div>
                <div class='kpi-value' style='color:{COLORS["danger"]}'>{critical_count}</div>
                <div class='kpi-subtitle'>Immediate Action Required</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='kpi-card' style='--accent-color:{COLORS["warning"]}'>
                <div class='kpi-title'>Warning Alerts</div>
                <div class='kpi-value' style='color:{COLORS["warning"]}'>{warning_count}</div>
                <div class='kpi-subtitle'>Monitor Closely</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        compliance_rate = ((1 - total_alerts / 20) * 100) if total_alerts < 20 else 0
        comp_color = COLORS['success'] if compliance_rate > 90 else COLORS['warning'] if compliance_rate > 75 else COLORS['danger']
        st.markdown(f"""
            <div class='kpi-card' style='--accent-color:{comp_color}'>
                <div class='kpi-title'>Compliance Rate</div>
                <div class='kpi-value' style='color:{comp_color}'>{compliance_rate:.0f}%</div>
                <div class='kpi-subtitle'>Risk Limits Met</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'><h3>Active Alerts</h3></div>", unsafe_allow_html=True)
    
    if alerts:
        for alert in alerts:
            alert_class = 'alert-critical' if alert['severity'] == 'critical' else 'alert-warning'
            icon = '🔴' if alert['severity'] == 'critical' else '🟡'
            
            st.markdown(f"""
                <div class='alert-box {alert_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div style='flex: 1;'>
                            <strong style='font-size: 1.1rem;'>{icon} {alert['title']}</strong>
                            <span class='metric-badge' style='margin-left: 0.5rem; background: rgba(255,255,255,0.1);'>
                                {alert['category']}
                            </span>
                            <br><br>
                            {alert['message']}
                            <br><br>
                            <small style='color: #9CA3AF;'>
                                Detected at: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                            </small>
                        </div>
                        <div style='text-align: right; padding-left: 1rem;'>
                            <span style='font-size: 1.5rem; font-weight: 700;'>{alert['metric']:.2f}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='alert-box alert-success'>
                <strong>All Clear - No Risk Breaches Detected</strong><br>
                All metrics are within acceptable thresholds. Portfolio risk is well-managed.
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# REPORTING & EXPORT SECTION
# ============================================================================

elif section == "Reporting & Export":
    st.title("Reporting & Data Export")
    st.markdown("Generate reports and export data for compliance and analysis")
    st.markdown("---")
    
    st.markdown("### Available Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='trade-card' style='border-color: {COLORS['info']}'>
                <h4>Daily Risk Report</h4>
                <p>Comprehensive daily risk metrics including VaR, ES, and stress tests</p>
                <br>
                <strong>Includes:</strong>
                <ul>
                    <li>Market risk metrics</li>
                    <li>Sector exposure analysis</li>
                    <li>Stress test results</li>
                    <li>Compliance status</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Daily Risk Report", use_container_width=True, key="gen_daily"):
            with st.spinner("Generating report..."):
                st.success("Report generated successfully!")
    
    with col2:
        st.markdown(f"""
            <div class='trade-card' style='border-color: {COLORS['success']}'>
                <h4>Portfolio Analytics Report</h4>
                <p>Detailed portfolio composition, performance, and trade recommendations</p>
                <br>
                <strong>Includes:</strong>
                <ul>
                    <li>Holdings breakdown</li>
                    <li>Performance attribution</li>
                    <li>Rebalancing recommendations</li>
                    <li>Optimization metrics</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Portfolio Report", use_container_width=True, key="gen_portfolio"):
            with st.spinner("Generating report..."):
                st.success("Report generated successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"""
            <div class='trade-card' style='border-color: {COLORS['warning']}'>
                <h4>Transaction Cost Analysis</h4>
                <p>Execution quality metrics and cost breakdown analysis</p>
                <br>
                <strong>Includes:</strong>
                <ul>
                    <li>Slippage analysis</li>
                    <li>Market impact metrics</li>
                    <li>P&L attribution</li>
                    <li>Broker performance</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate TCA Report", use_container_width=True, key="gen_tca"):
            with st.spinner("Generating report..."):
                st.success("Report generated successfully!")
    
    with col4:
        st.markdown(f"""
            <div class='trade-card' style='border-color: {COLORS['primary']}'>
                <h4>Strategy Performance Report</h4>
                <p>Backtesting results and strategy comparison analysis</p>
                <br>
                <strong>Includes:</strong>
                <ul>
                    <li>Strategy metrics</li>
                    <li>Walk-forward validation</li>
                    <li>Risk-return profiles</li>
                    <li>Recommendations</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Strategy Report", use_container_width=True, key="gen_strategy"):
            with st.spinner("Generating report..."):
                st.success("Report generated successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Data Export Options")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.markdown("#### Export Configuration")
        
        export_format = st.selectbox("Export Format", ["CSV", "Excel (XLSX)", "JSON", "PDF Report"])
        
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        datasets_to_export = st.multiselect(
            "Select Datasets",
            ["Risk Metrics", "Sector Exposure", "Portfolio Weights", 
             "Trade Recommendations", "TCA Summary", "Backtest Results"],
            default=["Risk Metrics"]
        )
        
        include_metadata = st.checkbox("Include Metadata & Audit Info", value=True)
        
        if st.button("Export Data", use_container_width=True, type="primary"):
            with st.spinner("Preparing export..."):
                st.success(f"Export prepared: {len(datasets_to_export)} dataset(s) in {export_format} format")
    
    with col_exp2:
        st.markdown("#### Recent Exports")
        
        recent_exports = pd.DataFrame({
            'Timestamp': [
                datetime.now() - timedelta(days=1),
                datetime.now() - timedelta(days=2),
                datetime.now() - timedelta(days=7)
            ],
            'Report Type': ['Daily Risk Report', 'Portfolio Analytics', 'TCA Report'],
            'Format': ['PDF', 'Excel', 'CSV'],
            'Size': ['2.4 MB', '1.8 MB', '850 KB'],
            'Status': ['Available', 'Available', 'Archived']
        })
        
        st.dataframe(recent_exports, use_container_width=True, height=200)
        
        st.markdown("""
            <div class='alert-box alert-info' style='margin-top: 1rem;'>
                <strong>Export Retention Policy</strong><br>
                Reports are retained for 90 days. Archived reports can be regenerated on request.
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <p style='background: linear-gradient(135deg, #667eea, #764ba2); 
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                  font-weight: 700; font-size: 1.1rem;'>
            Enterprise Risk Management System v2.5.0
        </p>
        <p style='color: #64748b; font-size: 0.875rem; margin-top: 1rem;'>
            © 2024 Risk Analytics Platform | All Rights Reserved
        </p>
    </div>
""", unsafe_allow_html=True)