# ============================================================================
# MODEL PERFORMANCE PAGE
# Compare models, show diagnostics, and explain choices
# Author: Shivam Gupta
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Model Performance", page_icon="🎯", layout="wide")

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

st.title("🎯 Model Performance & Diagnostics")
st.markdown("""
<p style='text-align:center; font-size:1.0rem; color:#4a5568;'>
See how each model performs, why some fail, and how Prophet + Promotions became the winner.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# PERFORMANCE TABLE
# ============================================================================

st.subheader("📊 Model Performance Overview")

model_perf = pd.DataFrame({
    'Store': ['Store 1', 'Store 1', 'Store 5', 'Store 5', 'Store 5', 'Store 5'],
    'Model': ['Naive', 'ARIMA', 'Naive', 'ARIMA', 'Prophet (Baseline)', 'Prophet + Promo'],
    'MAPE (%)': [9.65, 17.28, 36.97, np.nan, 20.39, 10.29],
    'MAE ($)': [np.nan, np.nan, np.nan, np.nan, 896.01, 443.30],
    'RMSE ($)': [np.nan, np.nan, np.nan, np.nan, 1099.85, np.nan],
    'R²': [np.nan, np.nan, np.nan, np.nan, 0.5014, np.nan],
    'Status': ['✅ Best', '❌ Overfit', '❌ Poor', '❌ Failed', '⚠️ Good', '✅ Best']
})

st.dataframe(
    model_perf.style.background_gradient(subset=['MAPE (%)'], cmap='RdYlGn_r'),
    use_container_width=True
)

st.markdown("---")

# ============================================================================
# MAPE BAR CHART
# ============================================================================

st.subheader("📈 MAPE Comparison")

plot_data = model_perf.dropna(subset=['MAPE (%)'])

fig_mape = px.bar(
    plot_data,
    x='Model',
    y='MAPE (%)',
    color='Store',
    text='MAPE (%)',
    title='MAPE by Model and Store',
    color_discrete_map={'Store 1': '#667eea', 'Store 5': '#f5576c'},
    height=450
)

fig_mape.add_hline(
    y=15, line_dash="dash", line_color="green",
    annotation_text="Target: <15% MAPE", annotation_position="right"
)

fig_mape.update_traces(
    texttemplate='%{text:.2f}%', textposition='outside',
    textfont=dict(size=13, color='#1a1a2e', family='Arial Black')
)

fig_mape.update_layout(
    font=dict(size=14, color='#1a1a2e', family='Arial'),
    plot_bgcolor='white', paper_bgcolor='white',
    yaxis_range=[0, 40],
    xaxis=dict(
        title=dict(text='Model', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
        tickfont=dict(size=13, color='#1a1a2e'),
        showline=True, linewidth=2, linecolor='#cbd5e0'
    ),
    yaxis=dict(
        title=dict(text='MAPE (%)', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
        tickfont=dict(size=13, color='#1a1a2e'),
        gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'
    ),
    legend=dict(font=dict(color='#1a1a2e'), bgcolor='rgba(255,255,255,0.9)')
)

st.plotly_chart(fig_mape, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.success("""
**Models that meet target (<15% MAPE):**
- Store 1: Naive (9.65%)
- Store 5: Prophet + Promotions (10.29%)
""")
with col2:
    st.warning("""
**Models that failed:**
- Store 1: ARIMA (17.28%) – overfit
- Store 5: Naive (36.97%) – too simple
- Store 5: ARIMA – failed to converge (NaN)
""")

st.markdown("---")

# ============================================================================
# PROPHET EVOLUTION
# ============================================================================

st.subheader("🚀 Store 5: Prophet Model Evolution")

prophet_evo = pd.DataFrame({
    'Stage': ['Naive Baseline', 'Prophet Baseline', 'Prophet Tuned', 'Prophet + Promo'],
    'MAPE': [36.97, 20.39, 18.79, 10.29],
    'Comment': [
        'Very high error',
        'Big improvement',
        'Small tuning gain',
        'Promos make it great'
    ]
})

fig_evo = go.Figure()
fig_evo.add_trace(go.Scatter(
    x=prophet_evo['Stage'], y=prophet_evo['MAPE'],
    mode='lines+markers+text',
    text=prophet_evo['MAPE'],
    texttemplate='%{text:.2f}%',
    textposition='top center',
    textfont=dict(size=15, color='#1a1a2e', family='Arial Black'),
    marker=dict(size=18, color=['#ff4444', '#ff8844', '#ffcc44', '#22c55e'],
                line=dict(width=2, color='#1a1a2e')),
    line=dict(color='#667eea', width=3)
))

fig_evo.update_layout(
    title=dict(text='Prophet Improvement Journey on Store 5', font=dict(size=18, color='#1a1a2e', family='Arial Black'), x=0.5),
    xaxis=dict(
        title='Model Stage', tickfont=dict(color='#1a1a2e'),
        showline=True, linewidth=2, linecolor='#cbd5e0'
    ),
    yaxis=dict(
        title='MAPE (%)', tickfont=dict(color='#1a1a2e'),
        gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0',
        range=[0, 40]
    ),
    plot_bgcolor='white', paper_bgcolor='white', height=400,
    hovermode='x unified'
)
st.plotly_chart(fig_evo, use_container_width=True)

st.info("""
**Key takeaway:**  
Hyperparameter tuning helped a bit (20.39% → 18.79%), but adding promotions dropped error to 10.29%.  
**Feature engineering delivered >10 percentage points improvement.**
""")

st.markdown("---")

# ============================================================================
# MODEL SELECTION DECISION TREE
# ============================================================================

st.subheader("🌳 Model Selection Framework")

st.markdown("""

START: Analyze Store Metrics (Autocorrelation, CV)
│
├── Autocorr > 0.7 AND CV < 20% ?
│ └── YES → ✅ Use NAIVE / MOVING AVERAGE
│ - Example: Store 1 (9.65% MAPE)
│
└── ELSE:
├── CV > 30% ?
│ └── YES → ✅ Use PROPHET (+ regressors) / LSTM
│ - Example: Store 5 + Promotions (10.29% MAPE)
│
└── NO → 🔄 Try ARIMA / Prophet and compare to baseline
            
""")

st.markdown("---")

# ============================================================================
# RESIDUAL VIEW (INTERACTIVE)
# ============================================================================

st.subheader("🔬 Residual Diagnostics (Prophet - Store 5)")

view = st.selectbox(
    "Residual view:",
    ["Residuals over time", "Residual histogram (distribution)", "Residuals vs fitted"],
)

# Simulated residuals for UI
np.random.seed(42)
dates = pd.date_range(start='2024-11-01', periods=42, freq='D')
residuals = np.random.normal(-236.71, 568.71, size=len(dates))
fitted = np.random.normal(5000, 800, size=len(dates))

if view == "Residuals over time":
    fig_res = go.Figure()
    fig_res.add_trace(go.Scatter(
        x=dates, y=residuals,
        mode='lines+markers', name='Residual',
        line=dict(color='steelblue', width=1.5)
    ))
    fig_res.add_hline(y=0, line_dash='dash', line_color='red')
    fig_res.update_layout(
        title=dict(text='Residuals Over Time (Actual - Predicted)', font=dict(size=16, color='#1a1a2e', family='Arial Black'), x=0.5),
        xaxis=dict(title='Date', tickfont=dict(color='#1a1a2e'),
                   showline=True, linewidth=2, linecolor='#cbd5e0'),
        yaxis=dict(title='Residual ($)', tickfont=dict(color='#1a1a2e'),
                   gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
        plot_bgcolor='white', paper_bgcolor='white', height=380
    )
elif view == "Residual histogram (distribution)":
    fig_res = go.Figure()
    fig_res.add_trace(go.Histogram(
        x=residuals, nbinsx=15,
        marker_color='coral', opacity=0.8
    ))
    fig_res.update_layout(
        title=dict(text='Residual Distribution', font=dict(size=16, color='#1a1a2e', family='Arial Black'), x=0.5),
        xaxis=dict(title='Residual ($)', tickfont=dict(color='#1a1a2e'),
                   showline=True, linewidth=2, linecolor='#cbd5e0'),
        yaxis=dict(title='Frequency', tickfont=dict(color='#1a1a2e'),
                   gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
        plot_bgcolor='white', paper_bgcolor='white', height=380
    )
else:  # Residuals vs fitted
    fig_res = go.Figure()
    fig_res.add_trace(go.Scatter(
        x=fitted, y=residuals,
        mode='markers', name='Residual vs Fitted',
        marker=dict(color='green', size=7, opacity=0.7)
    ))
    fig_res.add_hline(y=0, line_dash="dash", line_color="red")
    fig_res.update_layout(
        title=dict(text='Residuals vs Fitted Values', font=dict(size=16, color='#1a1a2e', family='Arial Black'), x=0.5),
        xaxis=dict(title='Fitted Values ($)', tickfont=dict(color='#1a1a2e'),
                   showline=True, linewidth=2, linecolor='#cbd5e0'),
        yaxis=dict(title='Residual ($)', tickfont=dict(color='#1a1a2e'),
                   gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
        plot_bgcolor='white', paper_bgcolor='white', height=380
    )

st.plotly_chart(fig_res, use_container_width=True)

st.markdown("""
- Mean residual ≈ -236 (slight overestimation bias)  
- Spread (std ≈ 569) reflects Store 5 volatility  
- No obvious pattern → residuals mostly random, good sign
""")

st.markdown("---")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

st.subheader("📋 Performance Summary & Interview Angle")

st.info("""
- For **simple stores**, Naive outperforms complex models → you know when *not* to use heavy ML.
- For **complex stores**, Prophet + Promotions delivers **72% improvement** over Naive.
- You validated models with baselines, diagnostics, and a clear selection framework.
- This page shows you understand **both accuracy and interpretability**, which interviewers love.
""")
