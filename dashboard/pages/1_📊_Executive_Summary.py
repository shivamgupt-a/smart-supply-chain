# ============================================================================
# EXECUTIVE SUMMARY PAGE
# High-level overview of entire project
# Author: Shivam Gupta
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")

# ============================================================================
# SHARED STYLING (MATCH app.py)
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

st.title("📊 Executive Summary")
st.markdown("""
<p style='text-align:center; font-size:1.05rem; color:#4a5568;'>
High-level overview of forecasting accuracy, store segmentation, and business impact.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# VIEW TOGGLE
# ============================================================================

view_mode = st.radio(
    "View perspective:",
    ["Overall Project", "Store 1 (Simple)", "Store 5 (Complex)"],
    horizontal=True
)

# ============================================================================
# KPI CARDS
# ============================================================================

col1, col2, col3 = st.columns(3)

if view_mode == "Overall Project":
    with col1:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>9.65%</div>
          <div class='metric-label'>Best MAPE</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Store 1 - Naive baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>10.29%</div>
          <div class='metric-label'>Best Complex Store MAPE</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Store 5 - Prophet + Promo</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>72%</div>
          <div class='metric-label'>Accuracy Improvement</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Store 5 vs Naive baseline</div>
        </div>
        """, unsafe_allow_html=True)
elif view_mode == "Store 1 (Simple)":
    with col1:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>9.65%</div>
          <div class='metric-label'>MAPE (Naive)</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Best model for Store 1</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>17.28%</div>
          <div class='metric-label'>MAPE (ARIMA)</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Overfitting vs Naive</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>Simple</div>
          <div class='metric-label'>Store Type</div>
          <div style='font-size:0.8rem;margin-top:8px;'>High autocorr, low volatility</div>
        </div>
        """, unsafe_allow_html=True)
else:  # Store 5
    with col1:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>36.97%</div>
          <div class='metric-label'>Naive MAPE</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Too simple for Store 5</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>10.29%</div>
          <div class='metric-label'>Prophet + Promo MAPE</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Best model for Store 5</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
          <div class='metric-value'>72%</div>
          <div class='metric-label'>Improvement vs Naive</div>
          <div style='font-size:0.8rem;margin-top:8px;'>Massive error reduction</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# STORE COMPLEXITY SCATTER
# ============================================================================

st.subheader("🏪 Store Complexity Segmentation")

complexity_data = {
    'Store': ['Store 1', 'Store 5'],
    'Autocorrelation': [0.95, 0.113],
    'CV (%)': [15, 37.74],
    'Complexity': ['Simple', 'Complex'],
    'Best_Model': ['Naive', 'Prophet + Promo'],
    'MAPE': [9.65, 10.29]
}
df_complexity = pd.DataFrame(complexity_data)

fig_complex = px.scatter(
    df_complexity,
    x='Autocorrelation',
    y='CV (%)',
    size='MAPE',
    color='Complexity',
    hover_data=['Store', 'Best_Model', 'MAPE'],
    title='Store Complexity Map: Data-Driven Model Selection',
    color_discrete_map={'Simple': 'green', 'Complex': 'red'},
    size_max=30
)

fig_complex.add_hline(y=20, line_dash="dash", line_color="orange",
                      annotation_text="CV = 20% threshold", annotation_position="top left")
fig_complex.add_vline(x=0.7, line_dash="dash", line_color="blue",
                      annotation_text="Autocorr = 0.7 threshold", annotation_position="bottom right")

fig_complex.update_layout(
    font=dict(size=14, color='#1a1a2e', family='Arial'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=dict(text='Autocorrelation (Lag 1)', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
        tickfont=dict(size=13, color='#1a1a2e'),
        showline=True, linewidth=2, linecolor='#cbd5e0'
    ),
    yaxis=dict(
        title=dict(text='Coefficient of Variation (%)', font=dict(size=15, color='#1a1a2e', family='Arial Black')),
        tickfont=dict(size=13, color='#1a1a2e'),
        gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'
    ),
    legend=dict(font=dict(color='#1a1a2e'))
)

st.plotly_chart(fig_complex, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.success("""
**Store 1 (Simple):**
- High autocorrelation (0.95) → predictable
- Low volatility (15% CV)
- Naive model (9.65% MAPE) is optimal
""")
with col2:
    st.warning("""
**Store 5 (Complex):**
- Low autocorrelation (0.113) → noisy
- High volatility (37.74% CV)
- Prophet + Promotions (10.29% MAPE) required
""")

st.markdown("---")

# ============================================================================
# MODEL PERFORMANCE TABLE + BAR
# ============================================================================

st.subheader("📈 Model Performance Across Stores")

model_performance = pd.DataFrame({
    'Store': ['Store 1', 'Store 1', 'Store 5', 'Store 5', 'Store 5'],
    'Model': ['Naive', 'ARIMA', 'Naive', 'Prophet', 'Prophet + Promo'],
    'MAPE (%)': [9.65, 17.28, 36.97, 20.39, 10.29],
    'Status': ['✅ Best', '❌ Overfit', '❌ Poor', '⚠️ Good', '✅ Best']
})

st.dataframe(model_performance.style.background_gradient(subset=['MAPE (%)'], cmap='RdYlGn_r'),
             use_container_width=True)

fig_mape = px.bar(
    model_performance,
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
    plot_bgcolor='white',
    paper_bgcolor='white',
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
    legend=dict(font=dict(color='#1a1a2e'), bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#cbd5e0', borderwidth=1)
)

st.plotly_chart(fig_mape, use_container_width=True)

st.markdown("---")

# ============================================================================
# KEY INSIGHTS
# ============================================================================

st.subheader("💡 Key Business Insights")

st.info("""
1. **Model selection must match store complexity.**  
   - Store 1: Naive (9.65% MAPE) beats ARIMA (17.28%).  
   - Store 5: Prophet + Promotions (10.29%) massively beats Naive (36.97%).

2. **Feature engineering outperforms pure tuning.**  
   - Prophet baseline: 20.39%  
   - Prophet tuned: 18.79%  
   - Prophet + Promo: 10.29% (10pp improvement from adding promo).

3. **Forecasts directly drive cost savings.**  
   - Inventory policies (EOQ, safety stock) built on forecasts  
   - Result: $XX,XXX annual savings at 95% service level.
""")

st.markdown("---")
