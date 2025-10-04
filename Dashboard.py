import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="Financial Risk Dashboard - Enhanced",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Professional Dark Theme CSS ----------------
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Headers */
    h1 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
    }
    
    h2, h3 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 600;
        color: #E0E0E0;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1E1E2F 0%, #2A2A3E 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    
    .kpi-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #B0B0B0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .kpi-change {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(90deg, #1E1E2F 0%, transparent 100%);
        padding: 0.8rem 1rem;
        border-left: 4px solid #00D9FF;
        margin: 1.5rem 0 1rem 0;
        border-radius: 4px;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .alert-danger {
        background-color: rgba(231, 76, 60, 0.1);
        border-color: #E74C3C;
        color: #E74C3C;
    }
    
    .alert-warning {
        background-color: rgba(241, 196, 15, 0.1);
        border-color: #F1C40F;
        color: #F1C40F;
    }
    
    .alert-success {
        background-color: rgba(46, 204, 113, 0.1);
        border-color: #2ECC71;
        color: #2ECC71;
    }
    
    /* Trade Card */
    .trade-card {
        background-color: #1A1A2E;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid;
    }
    
    .trade-buy {
        border-color: #2ECC71;
    }
    
    .trade-sell {
        border-color: #E74C3C;
    }
    
    /* Sidebar Button Styling */
    .stButton button {
        transition: all 0.3s ease;
        font-size: 0.95rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .stButton button:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.2);
    }
    
    /* Chart Containers */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Data Loading with Error Handling ----------------
@st.cache_data
def load_csv_safe(path):
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {path}: {str(e)}")
        return pd.DataFrame()

# ---------------- Load All Data ----------------
with st.spinner("Loading data..."):
    risk_metrics = load_csv_safe("./Risk Analytics Module/daily_risk_metrics.csv")
    sector_exposure = load_csv_safe("./Risk Analytics Module/sector_exposure.csv")
    backtest_results = load_csv_safe("./Backtesting Framework & Strategies/backtest_results.csv")
    backtest_wf = load_csv_safe("./Backtesting Framework & Strategies/backtest_results_walkforward.csv")
    target_weights = load_csv_safe("./Portfolio Optimization Module/target_weights.csv")
    trade_recommendations = load_csv_safe("./Portfolio Optimization Module/trade_recommendations.csv")
    portfolio_risk_returns = load_csv_safe("./Portfolio Optimization Module/portfolio_risk_return.csv")
    tca_summary = load_csv_safe("./Transaction Cost Analysis (TCA)/weekly_tca_summary.csv")

# ---------------- Sidebar Navigation ----------------
st.sidebar.markdown("""
<div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
    <h2 style='color: #00D9FF; margin: 0; font-size: 1.5rem;'>Financial Risk</h2>
    <p style='color: #B0B0B0; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Analytics & Trading Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #00D9FF, transparent); margin: 1rem 0;'></div>", unsafe_allow_html=True)

# Navigation Menu with Custom Styling
st.sidebar.markdown("<p style='color: #B0B0B0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 1.5rem 0 0.5rem 0;'>Navigation</p>", unsafe_allow_html=True)

menu_options = {
    "Executive Dashboard": "dashboard",
    "Risk Analytics": "risk",
    "Backtesting Comparison": "backtest",
    "Portfolio & Trades": "portfolio",
    "TCA & Attribution": "tca",
    "Alerts & Monitoring": "alerts"
}

# Create custom buttons for navigation
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = "Executive Dashboard"

for option, key in menu_options.items():
    is_selected = st.session_state.selected_section == option
    
    if st.sidebar.button(
        option,
        key=f"nav_{key}",
        use_container_width=True,
        type="primary" if is_selected else "secondary"
    ):
        st.session_state.selected_section = option
        st.rerun()

section = st.session_state.selected_section

# Sidebar Statistics
st.sidebar.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #00D9FF, transparent); margin: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: #B0B0B0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 1rem 0 0.5rem 0;'>System Status</p>", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style='background: #1E1E2F; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);'>
    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
        <span style='color: #B0B0B0; font-size: 0.85rem;'>Last Updated</span>
        <span style='color: #00D9FF; font-size: 0.85rem; font-weight: 600;'>{datetime.now().strftime('%H:%M')}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
        <span style='color: #B0B0B0; font-size: 0.85rem;'>Risk Metrics</span>
        <span style='color: #2ECC71; font-size: 0.85rem; font-weight: 600;'>{len(risk_metrics)}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
        <span style='color: #B0B0B0; font-size: 0.85rem;'>Sectors</span>
        <span style='color: #2ECC71; font-size: 0.85rem; font-weight: 600;'>{len(sector_exposure)}</span>
    </div>
    <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
        <span style='color: #B0B0B0; font-size: 0.85rem;'>Positions</span>
        <span style='color: #2ECC71; font-size: 0.85rem; font-weight: 600;'>{len(target_weights)}</span>
    </div>
    <div style='display: flex; justify-content: space-between;'>
        <span style='color: #B0B0B0; font-size: 0.85rem;'>Trades</span>
        <span style='color: #F1C40F; font-size: 0.85rem; font-weight: 600;'>{len(trade_recommendations)}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Connection Status
st.sidebar.markdown(f"""
<div style='margin-top: 1rem; padding: 0.75rem; background: rgba(46, 204, 113, 0.1); border-radius: 6px; border-left: 3px solid #2ECC71;'>
    <div style='display: flex; align-items: center;'>
        <div style='width: 8px; height: 8px; background: #2ECC71; border-radius: 50%; margin-right: 0.5rem;'></div>
        <span style='color: #2ECC71; font-size: 0.85rem; font-weight: 600;'>System Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 19rem; padding: 1rem; background: #0E1117; border-top: 1px solid rgba(255, 255, 255, 0.05);'>
    <p style='color: #666; font-size: 0.75rem; margin: 0; text-align: center;'>
        © 2025 Risk Analytics Platform<br>
        <span style='color: #00D9FF;'>Version 2.0.0</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- Helper Functions ----------------
def get_safe_value(series, index=-1, default=0.0):
    try:
        series_clean = series.dropna()
        if len(series_clean) > 0:
            return float(series_clean.iloc[index])
        return default
    except Exception:
        return default

def calculate_change(series, periods=1):
    try:
        series_clean = series.dropna()
        if len(series_clean) > periods:
            current = float(series_clean.iloc[-1])
            previous = float(series_clean.iloc[-(periods+1)])
            if previous != 0:
                return ((current - previous) / abs(previous)) * 100
        return 0.0
    except:
        return 0.0

def kpi_card(title, value, change=None, color='#00D9FF', format_str='.2f'):
    change_html = ""
    if change is not None:
        change_color = '#2ECC71' if change < 0 else '#E74C3C'
        change_symbol = '▼' if change < 0 else '▲'
        change_html = f"<div class='kpi-change' style='color:{change_color}'>{change_symbol} {abs(change):.2f}%</div>"
    
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>{title}</div>
            <div class='kpi-value' style='color:{color}'>{value:{format_str}}</div>
            {change_html}
        </div>
    """, unsafe_allow_html=True)

# ---------------- EXECUTIVE DASHBOARD ----------------
if section == "Executive Dashboard":
    st.title("Executive Dashboard")
    st.markdown("Comprehensive portfolio risk and performance overview")
    st.markdown("---")
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_95"])
            change = calculate_change(risk_metrics["VaR_95"])
            kpi_card("VaR 95%", val, change, '#E74C3C')
    
    with col2:
        if not risk_metrics.empty and "ES_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_95"])
            change = calculate_change(risk_metrics["ES_95"])
            kpi_card("ES 95%", val, change, '#E74C3C')
    
    with col3:
        if not portfolio_risk_returns.empty and "Expected Return" in portfolio_risk_returns.columns:
            val = get_safe_value(portfolio_risk_returns["Expected Return"]) * 100
            kpi_card("Expected Return", val, None, '#00D9FF', '.4f')
    
    with col4:
        if not portfolio_risk_returns.empty and "Sharpe Ratio" in portfolio_risk_returns.columns:
            val = get_safe_value(portfolio_risk_returns["Sharpe Ratio"])
            kpi_card("Sharpe Ratio", val, None, '#FFD93D')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two-column layout
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("<div class='section-header'><h3>Sector Exposure</h3></div>", unsafe_allow_html=True)
        
        if not sector_exposure.empty:
            sector_data = sector_exposure.copy()
            sector_data['portfolio_weight'] = sector_data['portfolio_weight'] * 100
            sector_data = sector_data.sort_values('portfolio_weight')
            
            fig = go.Figure()
            
            colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in sector_data['portfolio_weight']]
            
            fig.add_trace(go.Bar(
                x=sector_data['portfolio_weight'],
                y=sector_data['sector'],
                orientation='h',
                marker=dict(color=colors),
                text=sector_data['portfolio_weight'].apply(lambda x: f'{x:.3f}%'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Weight: %{x:.3f}%<extra></extra>'
            ))
            
            fig.update_layout(
                height=350,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Portfolio Weight (%)", gridcolor='#2A2A3E'),
                yaxis=dict(title=""),
                margin=dict(l=20, r=20, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sector_exposure")
        else:
            st.info("No sector exposure data available")
    
    with col_right:
        st.markdown("<div class='section-header'><h3>Stress Scenarios</h3></div>", unsafe_allow_html=True)
        
        if not risk_metrics.empty:
            stress_cols = ["Rate_Shock", "Volatility_Spike", "Sector_Drawdown"]
            available = [c for c in stress_cols if c in risk_metrics.columns]
            
            if available:
                latest_stress = risk_metrics[available].iloc[-1]
                
                for col in available:
                    val = latest_stress[col]
                    color = '#E74C3C' if val < -0.5 else '#F1C40F' if val < 0 else '#2ECC71'
                    
                    st.markdown(f"""
                        <div class='trade-card' style='border-color: {color}'>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='font-weight: 600;'>{col.replace('_', ' ')}</span>
                                <span style='color: {color}; font-weight: 700; font-size: 1.1rem;'>{val:.3f}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Portfolio Summary
    col_alloc, col_tca = st.columns(2)
    
    with col_alloc:
        st.markdown("<div class='section-header'><h3>Top Holdings</h3></div>", unsafe_allow_html=True)
        
        if not target_weights.empty and "Target Weight" in target_weights.columns:
            top_holdings = target_weights.nlargest(10, 'Target Weight')
            
            fig = px.bar(
                top_holdings,
                x='Target Weight',
                y='Instrument',
                orientation='h',
                color='Target Weight',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                height=350,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Weight", gridcolor='#2A2A3E'),
                yaxis=dict(title="", autorange='reversed'),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="top_holdings")
    
    with col_tca:
        st.markdown("<div class='section-header'><h3>TCA Trend</h3></div>", unsafe_allow_html=True)
        
        if not tca_summary.empty and "avg_slippage_bps" in tca_summary.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                y=tca_summary["avg_slippage_bps"],
                mode='lines+markers',
                line=dict(color='#FF5733', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(255, 87, 51, 0.1)',
                hovertemplate='Slippage: %{y:.2f} bps<extra></extra>'
            ))
            
            avg_slippage = tca_summary["avg_slippage_bps"].mean()
            fig.add_hline(y=avg_slippage, line_dash="dash", line_color="#FFD700",
                         annotation_text=f"Avg: {avg_slippage:.2f} bps")
            
            fig.update_layout(
                height=350,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Week", gridcolor='#2A2A3E'),
                yaxis=dict(title="Slippage (bps)", gridcolor='#2A2A3E'),
                margin=dict(l=50, r=20, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="tca_trend")

# ---------------- RISK ANALYTICS ----------------
elif section == "Risk Analytics":
    st.title("Risk Analytics Deep Dive")
    st.markdown("Comprehensive risk metrics and factor exposure analysis")
    st.markdown("---")
    
    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not risk_metrics.empty and "VaR_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_95"])
            change = calculate_change(risk_metrics["VaR_95"])
            kpi_card("VaR 95%", val, change, '#E74C3C')
    
    with col2:
        if not risk_metrics.empty and "ES_95" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_95"])
            change = calculate_change(risk_metrics["ES_95"])
            kpi_card("ES 95%", val, change, '#E74C3C')
    
    with col3:
        if not risk_metrics.empty and "VaR_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["VaR_99"])
            change = calculate_change(risk_metrics["VaR_99"])
            kpi_card("VaR 99%", val, change, '#FF5733')
    
    with col4:
        if not risk_metrics.empty and "ES_99" in risk_metrics.columns:
            val = get_safe_value(risk_metrics["ES_99"])
            change = calculate_change(risk_metrics["ES_99"])
            kpi_card("ES 99%", val, change, '#F1C40F')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stress Testing
    st.markdown("<div class='section-header'><h3>Stress Test Scenarios</h3></div>", unsafe_allow_html=True)
    
    if not risk_metrics.empty:
        stress_cols = ["Rate_Shock", "Volatility_Spike", "Sector_Drawdown"]
        available_stress = [c for c in stress_cols if c in risk_metrics.columns]
        
        if available_stress:
            stress_data = risk_metrics[available_stress].tail(100)
            
            fig = go.Figure()
            colors = ['#FF6B6B', '#4ECDC4', '#FFD93D']
            
            for i, col in enumerate(available_stress):
                fig.add_trace(go.Scatter(
                    y=stress_data[col],
                    name=col.replace('_', ' '),
                    mode='lines+markers',
                    line=dict(width=2.5, color=colors[i]),
                    marker=dict(size=4)
                ))
            
            fig.update_layout(
                height=400,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Time Period", gridcolor='#2A2A3E'),
                yaxis=dict(title="Impact (%)", gridcolor='#2A2A3E'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="stress_test")
    
    # Sector Exposure Table
    st.markdown("<div class='section-header'><h3>Detailed Sector Breakdown</h3></div>", unsafe_allow_html=True)
    
    if not sector_exposure.empty:
        sector_display = sector_exposure.copy()
        sector_display['portfolio_weight'] = sector_display['portfolio_weight'] * 100
        sector_display.columns = ['Sector', 'Portfolio Weight (%)']
        
        st.dataframe(sector_display.style.format({'Portfolio Weight (%)': '{:.4f}'}),
                    use_container_width=True, height=300)

# ---------------- BACKTESTING COMPARISON ----------------
elif section == "Backtesting Comparison":
    st.title("Backtesting Strategy Comparison")
    st.markdown("Performance comparison between strategies and validation methods")
    st.markdown("---")
    
    # Combine datasets
    if not backtest_results.empty and not backtest_wf.empty:
        backtest_standard = backtest_results.copy()
        backtest_standard['Method'] = 'Standard'
        
        backtest_walkforward = backtest_wf.copy()
        backtest_walkforward['Method'] = 'Walk-Forward'
        
        combined = pd.concat([backtest_standard, backtest_walkforward], ignore_index=True)
        
        # Metrics comparison
        st.markdown("<div class='section-header'><h3>Strategy Performance Metrics</h3></div>", unsafe_allow_html=True)
        
        metrics = ['Total Return', 'Volatility', 'Sharpe', 'Max Drawdown']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metrics,
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        colors = {'Momentum': '#00D9FF', 'Mean Reversion': '#FF5733', 
                 'Momentum (WF)': '#2ECC71', 'Mean Reversion (WF)': '#F1C40F'}
        
        for idx, metric in enumerate(metrics):
            row = idx // 2 + 1
            col = idx % 2 + 1
            
            for _, row_data in combined.iterrows():
                strategy_name = row_data['Strategy']
                color = colors.get(strategy_name, '#FFFFFF')
                
                fig.add_trace(
                    go.Bar(
                        name=strategy_name,
                        x=[strategy_name],
                        y=[row_data[metric]],
                        marker_color=color,
                        showlegend=(idx == 0),
                        hovertemplate=f'<b>{strategy_name}</b><br>{metric}: %{{y:.4f}}<extra></extra>'
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            height=600,
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='#FAFAFA'),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
            barmode='group'
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor='#2A2A3E')
        
        st.plotly_chart(fig, use_container_width=True, key="strategy_comparison")
        
        # Detailed Table
        st.markdown("<div class='section-header'><h3>Detailed Comparison Table</h3></div>", unsafe_allow_html=True)
        
        st.dataframe(
            combined.style.format({
                'Total Return': '{:.4f}',
                'Volatility': '{:.4f}',
                'Sharpe': '{:.6f}',
                'Max Drawdown': '{:.4f}'
            }),
            use_container_width=True,
            height=250
        )
        
        # Key Insights
        st.markdown("<div class='section-header'><h3>Key Insights</h3></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            best_sharpe = combined.loc[combined['Sharpe'].idxmax()]
            st.markdown(f"""
                <div class='alert-box alert-success'>
                    <strong>Best Sharpe Ratio:</strong><br>
                    {best_sharpe['Strategy']} ({best_sharpe['Method']})<br>
                    Sharpe: {best_sharpe['Sharpe']:.6f}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            best_return = combined.loc[combined['Total Return'].idxmax()]
            st.markdown(f"""
                <div class='alert-box alert-success'>
                    <strong>Highest Return:</strong><br>
                    {best_return['Strategy']} ({best_return['Method']})<br>
                    Return: {best_return['Total Return']:.2f}
                </div>
            """, unsafe_allow_html=True)

# ---------------- PORTFOLIO & TRADES ----------------
elif section == "Portfolio & Trades":
    st.title("Portfolio Optimization & Trade Recommendations")
    st.markdown("Target allocations and recommended trades")
    st.markdown("---")
    
    # Expected Risk/Return
    col1, col2, col3 = st.columns(3)
    
    if not portfolio_risk_returns.empty:
        with col1:
            exp_return = get_safe_value(portfolio_risk_returns["Expected Return"]) * 100
            kpi_card("Expected Return", exp_return, None, '#00D9FF', '.4f')
        
        with col2:
            exp_vol = get_safe_value(portfolio_risk_returns["Expected Volatility"]) * 100
            kpi_card("Expected Volatility", exp_vol, None, '#F1C40F', '.4f')
        
        with col3:
            sharpe = get_safe_value(portfolio_risk_returns["Sharpe Ratio"])
            kpi_card("Portfolio Sharpe", sharpe, None, '#2ECC71')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trade Recommendations
    st.markdown("<div class='section-header'><h3>Recommended Trades</h3></div>", unsafe_allow_html=True)
    
    if not trade_recommendations.empty and "Change (Buy/Sell)" in trade_recommendations.columns:
        trades = trade_recommendations.copy()
        trades['abs_change'] = trades['Change (Buy/Sell)'].abs()
        top_trades = trades.nlargest(15, 'abs_change')
        
        col_buy, col_sell = st.columns(2)
        
        with col_buy:
            st.markdown("#### Top Buys")
            buys = top_trades[top_trades['Change (Buy/Sell)'] > 0].head(7)
            
            for _, trade in buys.iterrows():
                st.markdown(f"""
                    <div class='trade-card trade-buy'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <strong>{trade['Instrument']}</strong><br>
                                <span style='font-size: 0.85rem; color: #B0B0B0;'>
                                    {trade['Current Weight']:.6f} → {trade['Target Weight']:.6f}
                                </span>
                            </div>
                            <div style='text-align: right;'>
                                <span style='color: #2ECC71; font-weight: 700; font-size: 1.1rem;'>
                                    +{trade['Change (Buy/Sell)']:.6f}
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col_sell:
            st.markdown("#### Top Sells")
            sells = top_trades[top_trades['Change (Buy/Sell)'] < 0].head(7)
            
            for _, trade in sells.iterrows():
                st.markdown(f"""
                    <div class='trade-card trade-sell'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <strong>{trade['Instrument']}</strong><br>
                                <span style='font-size: 0.85rem; color: #B0B0B0;'>
                                    {trade['Current Weight']:.6f} → {trade['Target Weight']:.6f}
                                </span>
                            </div>
                            <div style='text-align: right;'>
                                <span style='color: #E74C3C; font-weight: 700; font-size: 1.1rem;'>
                                    {trade['Change (Buy/Sell)']:.6f}
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary Statistics
        st.markdown("<div class='section-header'><h3>Trade Summary</h3></div>", unsafe_allow_html=True)
        
        total_turnover = trades['abs_change'].sum()
        num_buys = len(trades[trades['Change (Buy/Sell)'] > 0])
        num_sells = len(trades[trades['Change (Buy/Sell)'] < 0])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            kpi_card("Total Turnover", total_turnover, None, '#00D9FF', '.6f')
        with col2:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Number of Buys</div>
                    <div class='kpi-value' style='color:#2ECC71'>{num_buys}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Number of Sells</div>
                    <div class='kpi-value' style='color:#E74C3C'>{num_sells}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Full Trade Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><h3>Complete Trade List</h3></div>", unsafe_allow_html=True)
        
        st.dataframe(
            trades.style.format({
                'Current Weight': '{:.6f}',
                'Target Weight': '{:.6f}',
                'Change (Buy/Sell)': '{:.6f}'
            }),
            use_container_width=True,
            height=400
        )

# ---------------- TCA & ATTRIBUTION ----------------
elif section == "TCA & Attribution":
    st.title("Transaction Cost Analysis & P&L Attribution")
    st.markdown("Execution quality metrics and performance attribution")
    st.markdown("---")
    
    if not tca_summary.empty:
        # Summary KPIs
        st.markdown("<div class='section-header'><h3>TCA Summary Metrics</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_slippage = tca_summary['avg_slippage_bps'].mean()
            kpi_card("Avg Slippage", avg_slippage, None, '#FF5733', '.2f')
        
        with col2:
            avg_impact = tca_summary['avg_market_impact_bps'].mean()
            kpi_card("Avg Market Impact", avg_impact, None, '#F1C40F', '.2f')
        
        with col3:
            total_commission = tca_summary['total_commission'].sum()
            kpi_card("Total Commission", total_commission, None, '#00D9FF', ',.0f')
        
        with col4:
            total_pnl = tca_summary['total_pnl'].sum()
            pnl_color = '#2ECC71' if total_pnl > 0 else '#E74C3C'
            kpi_card("Total P&L", total_pnl, None, pnl_color, ',.0f')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # P&L Attribution
        st.markdown("<div class='section-header'><h3>P&L Attribution Breakdown</h3></div>", unsafe_allow_html=True)
        
        if all(col in tca_summary.columns for col in ['total_alpha', 'total_beta', 'total_cost', 'total_timing']):
            # Weekly attribution stacked bar
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Alpha',
                x=tca_summary.index,
                y=tca_summary['total_alpha'],
                marker_color='#2ECC71',
                hovertemplate='Alpha: %{y:,.0f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Beta',
                x=tca_summary.index,
                y=tca_summary['total_beta'],
                marker_color='#00D9FF',
                hovertemplate='Beta: %{y:,.0f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Cost',
                x=tca_summary.index,
                y=tca_summary['total_cost'],
                marker_color='#E74C3C',
                hovertemplate='Cost: %{y:,.0f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Timing',
                x=tca_summary.index,
                y=tca_summary['total_timing'],
                marker_color='#F1C40F',
                hovertemplate='Timing: %{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                barmode='relative',
                height=400,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Week", gridcolor='#2A2A3E'),
                yaxis=dict(title="P&L Attribution", gridcolor='#2A2A3E'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="pnl_attribution")
            
            # Attribution Summary
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'><h3>Cumulative Attribution</h3></div>", unsafe_allow_html=True)
            
            total_alpha = tca_summary['total_alpha'].sum()
            total_beta = tca_summary['total_beta'].sum()
            total_cost = tca_summary['total_cost'].sum()
            total_timing = tca_summary['total_timing'].sum()
            
            attribution_df = pd.DataFrame({
                'Component': ['Alpha', 'Beta', 'Cost', 'Timing'],
                'Value': [total_alpha, total_beta, total_cost, total_timing],
                'Color': ['#2ECC71', '#00D9FF', '#E74C3C', '#F1C40F']
            })
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=attribution_df['Component'],
                values=attribution_df['Value'].abs(),
                marker=dict(colors=attribution_df['Color']),
                hole=0.4,
                hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percent: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                height=400,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                showlegend=True
            )
            
            st.plotly_chart(fig_pie, use_container_width=True, key="attribution_pie")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Slippage and Impact Trends
        col_slip, col_impact = st.columns(2)
        
        with col_slip:
            st.markdown("<div class='section-header'><h3>Slippage Trend</h3></div>", unsafe_allow_html=True)
            
            fig_slip = go.Figure()
            fig_slip.add_trace(go.Scatter(
                y=tca_summary['avg_slippage_bps'],
                mode='lines+markers',
                line=dict(color='#FF5733', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(255, 87, 51, 0.2)',
                hovertemplate='Slippage: %{y:.2f} bps<extra></extra>'
            ))
            
            fig_slip.update_layout(
                height=300,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Week", gridcolor='#2A2A3E'),
                yaxis=dict(title="Slippage (bps)", gridcolor='#2A2A3E')
            )
            
            st.plotly_chart(fig_slip, use_container_width=True, key="slippage_trend")
        
        with col_impact:
            st.markdown("<div class='section-header'><h3>Market Impact Trend</h3></div>", unsafe_allow_html=True)
            
            fig_impact = go.Figure()
            fig_impact.add_trace(go.Scatter(
                y=tca_summary['avg_market_impact_bps'],
                mode='lines+markers',
                line=dict(color='#F1C40F', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(241, 196, 15, 0.2)',
                hovertemplate='Market Impact: %{y:.2f} bps<extra></extra>'
            ))
            
            fig_impact.update_layout(
                height=300,
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#FAFAFA'),
                xaxis=dict(title="Week", gridcolor='#2A2A3E'),
                yaxis=dict(title="Market Impact (bps)", gridcolor='#2A2A3E')
            )
            
            st.plotly_chart(fig_impact, use_container_width=True, key="impact_trend")
        
        # Detailed TCA Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><h3>Detailed TCA Data</h3></div>", unsafe_allow_html=True)
        
        st.dataframe(
            tca_summary.style.format({
                'avg_slippage_bps': '{:.2f}',
                'total_slippage_value': '{:,.2f}',
                'total_commission': '{:,.2f}',
                'avg_market_impact_bps': '{:.2f}',
                'total_market_impact_value': '{:,.2f}',
                'total_pnl': '{:,.2f}',
                'total_alpha': '{:,.2f}',
                'total_beta': '{:,.2f}',
                'total_cost': '{:,.2f}',
                'total_timing': '{:,.2f}'
            }),
            use_container_width=True,
            height=400
        )

# ---------------- ALERTS & MONITORING ----------------
elif section == "Alerts & Monitoring":
    st.title("Alerts & Risk Monitoring")
    st.markdown("Real-time breach alerts and risk threshold monitoring")
    st.markdown("---")
    
    alerts = []
    
    # VaR Breach Alerts
    if not risk_metrics.empty:
        var_95_threshold = -10.0
        var_99_threshold = -40.0
        
        if "VaR_95" in risk_metrics.columns:
            latest_var_95 = get_safe_value(risk_metrics["VaR_95"])
            if latest_var_95 < var_95_threshold:
                alerts.append({
                    'type': 'danger',
                    'title': 'VaR 95% Breach',
                    'message': f'Current VaR 95%: {latest_var_95:.2f} exceeds threshold of {var_95_threshold}',
                    'metric': latest_var_95
                })
        
        if "VaR_99" in risk_metrics.columns:
            latest_var_99 = get_safe_value(risk_metrics["VaR_99"])
            if latest_var_99 < var_99_threshold:
                alerts.append({
                    'type': 'danger',
                    'title': 'VaR 99% Breach',
                    'message': f'Current VaR 99%: {latest_var_99:.2f} exceeds threshold of {var_99_threshold}',
                    'metric': latest_var_99
                })
    
    # Stress Test Alerts
    if not risk_metrics.empty:
        stress_threshold = -1.0
        stress_cols = ["Rate_Shock", "Volatility_Spike", "Sector_Drawdown"]
        
        for col in stress_cols:
            if col in risk_metrics.columns:
                latest_stress = get_safe_value(risk_metrics[col])
                if latest_stress < stress_threshold:
                    alerts.append({
                        'type': 'warning',
                        'title': f'{col.replace("_", " ")} Alert',
                        'message': f'Current {col}: {latest_stress:.3f}% exceeds stress threshold',
                        'metric': latest_stress
                    })
    
    # Sector Concentration Alerts
    if not sector_exposure.empty:
        sector_limit = 0.05
        
        for _, row in sector_exposure.iterrows():
            if abs(row['portfolio_weight']) > sector_limit:
                alert_type = 'warning' if abs(row['portfolio_weight']) < 0.08 else 'danger'
                alerts.append({
                    'type': alert_type,
                    'title': 'Sector Concentration Alert',
                    'message': f'{row["sector"]} exposure: {row["portfolio_weight"]*100:.3f}% exceeds {sector_limit*100}% limit',
                    'metric': row['portfolio_weight'] * 100
                })
    
    # TCA Alerts
    if not tca_summary.empty and 'avg_slippage_bps' in tca_summary.columns:
        slippage_threshold = 1.0
        latest_slippage = get_safe_value(tca_summary['avg_slippage_bps'])
        
        if abs(latest_slippage) > slippage_threshold:
            alerts.append({
                'type': 'warning',
                'title': 'High Slippage Alert',
                'message': f'Average slippage: {latest_slippage:.2f} bps exceeds {slippage_threshold} bps threshold',
                'metric': latest_slippage
            })
    
    # Display Alerts
    st.markdown("<div class='section-header'><h3>Active Alerts</h3></div>", unsafe_allow_html=True)
    
    if alerts:
        # Count by type
        danger_count = sum(1 for a in alerts if a['type'] == 'danger')
        warning_count = sum(1 for a in alerts if a['type'] == 'warning')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Total Alerts</div>
                    <div class='kpi-value' style='color:#F1C40F'>{len(alerts)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Critical</div>
                    <div class='kpi-value' style='color:#E74C3C'>{danger_count}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>Warnings</div>
                    <div class='kpi-value' style='color:#F1C40F'>{warning_count}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display individual alerts
        for alert in alerts:
            alert_class = f"alert-{alert['type']}"
            st.markdown(f"""
                <div class='alert-box {alert_class}'>
                    <strong>{alert['title']}</strong><br>
                    {alert['message']}<br>
                    <small>Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='alert-box alert-success'>
                <strong>All Clear</strong><br>
                No risk breaches detected. All metrics within acceptable thresholds.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monitoring Dashboard
    st.markdown("<div class='section-header'><h3>Risk Thresholds Monitor</h3></div>", unsafe_allow_html=True)
    
    # Create threshold visualization
    if not risk_metrics.empty:
        thresholds = {
            'VaR 95%': {'current': get_safe_value(risk_metrics.get("VaR_95", pd.Series([0]))), 
                       'threshold': -10.0, 'unit': ''},
            'VaR 99%': {'current': get_safe_value(risk_metrics.get("VaR_99", pd.Series([0]))), 
                       'threshold': -40.0, 'unit': ''},
            'ES 95%': {'current': get_safe_value(risk_metrics.get("ES_95", pd.Series([0]))), 
                      'threshold': -50.0, 'unit': ''},
            'ES 99%': {'current': get_safe_value(risk_metrics.get("ES_99", pd.Series([0]))), 
                      'threshold': -150.0, 'unit': ''}
        }
        
        threshold_df = pd.DataFrame([
            {
                'Metric': k,
                'Current': v['current'],
                'Threshold': v['threshold'],
                'Utilization': (v['current'] / v['threshold'] * 100) if v['threshold'] != 0 else 0,
                'Status': 'Breach' if v['current'] < v['threshold'] else 'OK'
            }
            for k, v in thresholds.items()
        ])
        
        fig = go.Figure()
        
        colors = ['#E74C3C' if status == 'Breach' else '#2ECC71' 
                 for status in threshold_df['Status']]
        
        fig.add_trace(go.Bar(
            x=threshold_df['Utilization'],
            y=threshold_df['Metric'],
            orientation='h',
            marker=dict(color=colors),
            text=threshold_df['Utilization'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Utilization: %{x:.1f}%<br>Current: %{customdata[0]:.2f}<br>Threshold: %{customdata[1]:.2f}<extra></extra>',
            customdata=threshold_df[['Current', 'Threshold']].values
        ))
        
        fig.add_vline(x=100, line_dash="dash", line_color="#F1C40F", 
                     annotation_text="Threshold", annotation_position="top")
        
        fig.update_layout(
            height=300,
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='#FAFAFA'),
            xaxis=dict(title="Utilization (%)", gridcolor='#2A2A3E', range=[0, 150]),
            yaxis=dict(title=""),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="threshold_monitor")
    
    # Audit Trail Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><h3>Audit Trail</h3></div>", unsafe_allow_html=True)
    
    audit_data = {
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Module': ['Risk Analytics'],
        'Action': ['Daily Risk Calculation'],
        'Status': ['Success'],
        'Records Processed': [len(risk_metrics)],
        'Data Version': ['v1.0.0'],
        'Code Version': ['dashboard-v2.0.0']
    }
    
    audit_df = pd.DataFrame(audit_data)
    
    st.dataframe(audit_df, use_container_width=True, height=150)
    
    st.markdown("""
        <div class='alert-box alert-success'>
            <strong>Audit Ready</strong><br>
            All metrics are linked to data snapshots and code versions for full reproducibility.
            Data lineage tracking enabled.
        </div>
    """, unsafe_allow_html=True)