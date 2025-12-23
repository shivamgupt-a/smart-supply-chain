# ============================================================================
# DEMAND FORECASTING PAGE
# Interactive forecasts and store comparison
# Author: Shivam Gupta
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta

st.set_page_config(page_title="Demand Forecasting", page_icon="📈", layout="wide")

# ============================================================================
# SHARED STYLING
# ============================================================================

st.markdown("""
    <style>
    .main {
        background: #f5f7fa;
        padding: 0rem 1rem;
    }
    .block-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        max-width: 1400px;
        margin: 0 auto;
    }
    h1 {
        color: #1a1a2e !important;
        font-weight: 800 !important;
        text-align: center;
        font-size: 2.6rem !important;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    h2 {
        color: #1a1a2e !important;
        border-bottom: 3px solid #667eea;
        padding-bottom: 8px;
        margin-top: 25px;
        font-weight: 700 !important;
    }
    h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    p, li, span {
        color: #4a5568 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 18px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    .metric-value {
        font-size: 2.0rem;
        font-weight: bold;
        color: #FFD700;
    }
    .metric-label {
        font-size: 0.9rem;
        margin-top: 5px;
        color: white;
        font-weight: 500;
    }
    .dataframe thead tr th {
        background: #667eea !important;
        color: white !important;
    }
    .dataframe tbody tr td {
        color: #2d3748 !important;
    }
    
    /* ========== SIDEBAR GRADIENT FIX ========== */
    
    /* Main sidebar container */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar content wrapper */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* All text in sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar links (page navigation) */
    [data-testid="stSidebar"] a {
        color: white !important;
        text-decoration: none !important;
    }
    
    [data-testid="stSidebar"] a:hover {
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    /* Active page highlight */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
    
    /* Sidebar header */
    section[data-testid="stSidebar"] header {
        background: transparent !important;
    }
    
    /* Sidebar widgets (selectbox, radio, etc.) */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Make sure page links are visible */
    .css-1544g2n {
        background: transparent !important;
    }
    
    /* Navigation link styling */
    [data-testid="stSidebarNav"] {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 10px !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebarNav"] a {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateX(5px) !important;
    }
    
    /* Active page */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255, 215, 0, 0.3) !important;
        font-weight: bold !important;
        border-left: 4px solid #FFD700 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# TITLE
# ============================================================================

st.title("📈 Demand Forecasting")
st.markdown("""
<p style='text-align:center; font-size:1.0rem; color:#4a5568;'>
Explore historical sales, forecasts, and what-if scenarios for each store.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SETTINGS
# ============================================================================

mode = st.radio(
    "Forecast mode:",
    ["Single Store", "Compare Store 1 vs Store 5"],
    horizontal=True
)

show_ma = st.checkbox("Show 7-day moving average", value=True)

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_store_data(store_num: int):
    path = f"C:/Users/Shivam Gupta/Coding/smart-supply-chain/data/processed/store_{store_num}_data.csv"
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df[df['Open'] == 1].copy()
    df = df.sort_values('Date')
    return df

# ============================================================================
# SINGLE STORE MODE
# ============================================================================

if mode == "Single Store":
    col_left, col_right = st.columns([1, 3])

    with col_left:
        store_choice = st.selectbox(
            "Select store:",
            ["Store 1 (Simple)", "Store 5 (Complex)"]
        )
        horizon = st.slider("Forecast horizon (days):", 7, 30, 14, step=7)
        show_ci = st.checkbox("Show confidence interval", value=True)

    store_num = 1 if "Store 1" in store_choice else 5
    df_store = load_store_data(store_num)

    if store_num == 1:
        best_model = "Naive"
        best_mape = 9.65
        model_color = "green"
    else:
        best_model = "Prophet + Promotions"
        best_mape = 10.29
        model_color = "red"

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-value'>{best_model}</div>
          <div class='metric-label'>Best Model</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-value'>{best_mape:.2f}%</div>
          <div class='metric-label'>MAPE</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-value'>${df_store['Sales'].mean():.0f}</div>
          <div class='metric-label'>Avg Daily Sales</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-value'>{len(df_store)}</div>
          <div class='metric-label'>Data Points</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Historical chart
    st.subheader("📊 Historical Sales")

    df_store['MA7'] = df_store['Sales'].rolling(window=7).mean()

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=df_store['Date'], y=df_store['Sales'],
        mode='lines', name='Daily Sales',
        line=dict(color='steelblue', width=1.5)
    ))
    if show_ma:
        fig_hist.add_trace(go.Scatter(
            x=df_store['Date'], y=df_store['MA7'],
            mode='lines', name='7-day MA',
            line=dict(color='orange', width=2)
        ))

    fig_hist.update_layout(
        title=dict(text=f"{store_choice} - Historical Sales", font=dict(size=18, color='#1a1a2e', family='Arial Black'), x=0.5),
        xaxis=dict(
            title=dict(text='Date', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
            tickfont=dict(size=13, color='#1a1a2e'),
            showline=True, linewidth=2, linecolor='#cbd5e0'
        ),
        yaxis=dict(
            title=dict(text='Sales ($)', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
            tickfont=dict(size=13, color='#1a1a2e'),
            gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'
        ),
        plot_bgcolor='white', paper_bgcolor='white', height=430,
        hovermode='x unified', legend=dict(font=dict(color='#1a1a2e'))
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # Forecast (simulated for UI; real app: load from saved Prophet outputs)
    st.subheader(f"🔮 {horizon}-Day Forecast ({best_model})")

    last_date = df_store['Date'].max()
    future_dates = pd.date_range(last_date + timedelta(days=1), periods=horizon, freq='D')
    recent = df_store.tail(30)
    mu, sigma = recent['Sales'].mean(), recent['Sales'].std()

    base_forecast = np.random.normal(mu, sigma * 0.4, size=horizon)

    if store_num == 5:
        st.markdown("**What-if analysis: change promotion uplift assumption**")
        promo_boost = st.slider(
            "Assumed promotion uplift (%)",
            min_value=0, max_value=80, value=45, step=5
        )
        promo_factor = 1 + promo_boost / 100
        promo_forecast = base_forecast * promo_factor
    else:
        promo_forecast = None

    # Confidence interval
    ci_width = sigma * 0.3
    lower = base_forecast - 1.96 * ci_width
    upper = base_forecast + 1.96 * ci_width

    fig_fore = go.Figure()

    hist_context = df_store.tail(60)
    fig_fore.add_trace(go.Scatter(
        x=hist_context['Date'], y=hist_context['Sales'],
        mode='lines', name='Historical',
        line=dict(color='steelblue', width=1.5)
    ))
    fig_fore.add_trace(go.Scatter(
        x=future_dates, y=base_forecast,
        mode='lines+markers', name='Forecast (Base)',
        line=dict(color=model_color, width=2, dash='dash'),
        marker=dict(size=6)
    ))

    if show_ci:
        fig_fore.add_trace(go.Scatter(
            x=future_dates, y=upper,
            mode='lines', line=dict(width=0), showlegend=False
        ))
        fig_fore.add_trace(go.Scatter(
            x=future_dates, y=lower,
            mode='lines', line=dict(width=0),
            fill='tonexty', fillcolor='rgba(102,126,234,0.2)',
            name='95% CI'
        ))

    if promo_forecast is not None:
        fig_fore.add_trace(go.Scatter(
            x=future_dates, y=promo_forecast,
            mode='lines+markers', name=f'Forecast with {promo_boost}% promo uplift',
            line=dict(color='orange', width=2),
            marker=dict(size=5, symbol='triangle-up')
        ))

    fig_fore.update_layout(
        title=dict(text=f"{store_choice} - {horizon}-Day Forecast", font=dict(size=18, color='#1a1a2e', family='Arial Black'), x=0.5),
        xaxis=dict(
            title=dict(text='Date', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
            tickfont=dict(size=13, color='#1a1a2e'),
            showline=True, linewidth=2, linecolor='#cbd5e0'
        ),
        yaxis=dict(
            title=dict(text='Sales ($)', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
            tickfont=dict(size=13, color='#1a1a2e'),
            gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'
        ),
        plot_bgcolor='white', paper_bgcolor='white', height=430,
        hovermode='x unified',
        legend=dict(font=dict(color='#1a1a2e'), bgcolor='rgba(255,255,255,0.9)')
    )

    st.plotly_chart(fig_fore, use_container_width=True)

    # Forecast table + download
    st.subheader("📋 Forecast Table")
    df_forecast = pd.DataFrame({
        'Date': future_dates,
        'Forecast_Base': base_forecast.round(2),
        'Lower_95%': lower.round(2),
        'Upper_95%': upper.round(2)
    })
    if promo_forecast is not None:
        df_forecast['Forecast_With_Promo'] = promo_forecast.round(2)

    st.dataframe(df_forecast, use_container_width=True)
    csv = df_forecast.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Forecast CSV",
        data=csv,
        file_name=f'forecast_store{store_num}_{horizon}d.csv',
        mime='text/csv'
    )

    st.markdown("---")

    st.subheader("💡 Model Insight")

    if store_num == 1:
        st.success("""
**Store 1 - Why Naive works:**
- Very high autocorrelation: tomorrow ≈ today
- Low volatility, stable weekly pattern
- Naive (9.65% MAPE) beats ARIMA (17.28%)
- Simple, fast, and robust → perfect for stable stores
""")
    else:
        st.warning("""
**Store 5 - Why Prophet + Promo is needed:**
- High volatility (CV 37.74%), low autocorr
- Naive error is huge (36.97% MAPE)
- Prophet baseline drops error to 20.39%
- Adding promotions as regressor → 10.29% MAPE
- Domain knowledge (promos) beats pure tuning
""")

# ============================================================================
# COMPARISON MODE
# ============================================================================

else:
    st.subheader("📊 Store 1 vs Store 5 - Side-by-Side")

    st.markdown("""
Compare a simple stable store (Store 1) with a complex volatile store (Store 5).  
This clearly shows **why different models are needed**.
""")

    df1 = load_store_data(1)
    df5 = load_store_data(5)

    lookback = st.slider("Look-back window (days):", 30, 120, 60, step=15)

    col_left, col_right = st.columns(2)

    # Store 1 chart
    with col_left:
        st.markdown("### Store 1 (Simple) - Naive")
        df1_recent = df1.tail(lookback)
        df1_recent['MA7'] = df1_recent['Sales'].rolling(window=7).mean()

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df1_recent['Date'], y=df1_recent['Sales'],
            mode='lines', name='Sales', line=dict(color='steelblue', width=1.5)
        ))
        fig1.add_trace(go.Scatter(
            x=df1_recent['Date'], y=df1_recent['MA7'],
            mode='lines', name='7-day MA', line=dict(color='orange', width=2)
        ))
        fig1.update_layout(
            title=dict(text='Store 1 - Stable Pattern', font=dict(size=16, color='#1a1a2e', family='Arial Black'), x=0.5),
            xaxis=dict(title='Date', tickfont=dict(color='#1a1a2e'),
                       showline=True, linewidth=2, linecolor='#cbd5e0'),
            yaxis=dict(title='Sales ($)', tickfont=dict(color='#1a1a2e'),
                       gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
            plot_bgcolor='white', paper_bgcolor='white', height=350,
            legend=dict(font=dict(color='#1a1a2e'))
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.success("""
**Key point:**
- Clear weekly pattern, low noise
- Naive forecast is sufficient and optimal here
""")

    # Store 5 chart
    with col_right:
        st.markdown("### Store 5 (Complex) - Prophet + Promo")
        df5_recent = df5.tail(lookback)
        df5_recent['MA7'] = df5_recent['Sales'].rolling(window=7).mean()

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df5_recent['Date'], y=df5_recent['Sales'],
            mode='lines', name='Sales', line=dict(color='firebrick', width=1.5)
        ))
        fig2.add_trace(go.Scatter(
            x=df5_recent['Date'], y=df5_recent['MA7'],
            mode='lines', name='7-day MA', line=dict(color='orange', width=2)
        ))
        fig2.update_layout(
            title=dict(text='Store 5 - Volatile Pattern', font=dict(size=16, color='#1a1a2e', family='Arial Black'), x=0.5),
            xaxis=dict(title='Date', tickfont=dict(color='#1a1a2e'),
                       showline=True, linewidth=2, linecolor='#cbd5e0'),
            yaxis=dict(title='Sales ($)', tickfont=dict(color='#1a1a2e'),
                       gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
            plot_bgcolor='white', paper_bgcolor='white', height=350,
            legend=dict(font=dict(color='#1a1a2e'))
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.warning("""
**Key point:**
- Noisy, spiky demand pattern
- Naive fails badly → need Prophet + promotions
""")

    st.markdown("---")

    st.subheader("💡 Interview Talking Point")
    st.info("""
This page demonstrates:
- How forecasts behave for **different store types**
- Why simple models are enough for stable stores
- Why advanced models are required for volatile stores
- A clear visual story recruiters understand quickly
""")
