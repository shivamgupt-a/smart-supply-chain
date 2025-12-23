# ============================================================================
# SUPPLY CHAIN FORECASTING DASHBOARD - PROFESSIONAL VERSION
# Main Application Entry Point
# Author: Shivam Gupta
# Date: December 2024
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Supply Chain Forecasting | Shivam Gupta",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CUSTOM CSS - FIXED CONTRAST
# ============================================================================

st.markdown("""
    <style>
    /* Remove gradient background, use solid white */
    .main {
        background: #f5f7fa;
        padding: 0rem 1rem;
    }
    
    /* Content container - white background */
    .block-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        margin: 10px 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 1;
        margin-top: 5px;
        color: white;
        font-weight: 500;
    }
    
    /* Header styling - FIXED COLORS */
    h1 {
        color: #1a1a2e !important;
        font-weight: 800 !important;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 10px;
        text-shadow: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: #1a1a2e !important;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-top: 30px;
        font-weight: 700 !important;
    }
    
    h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    /* Paragraph text */
    p {
        color: #4a5568 !important;
    }
    
    /* Info boxes with better contrast */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        color: #1a1a2e !important;
    }
    
    .dataframe thead tr th {
        background: #667eea !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .dataframe tbody tr td {
        color: #2d3748 !important;
    }
    
    /* Animation for metrics */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #4a5568 !important;
        margin-top: 50px;
        border-top: 2px solid #e2e8f0;
    }
    
    .footer a {
        color: #667eea !important;
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer a:hover {
        color: #764ba2 !important;
        text-decoration: underline;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Streamlit native elements */
    .stMarkdown {
        color: #2d3748 !important;
    }
    
    /* Metric native widget fix */
    [data-testid="stMetricValue"] {
        color: #1a1a2e !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a5568 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - ENHANCED
# ============================================================================

with st.sidebar:
    st.markdown("<h1 style='color: white; text-align: center;'>📦</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; text-align: center;'>Supply Chain Analytics</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Real-time clock
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%B %d, %Y")
    
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 1.5rem; font-weight: bold;'>{current_time}</div>
        <div style='font-size: 0.9rem; opacity: 0.8;'>{current_date}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project stats
    st.markdown("""
    <div style='color: white;'>
        <h4>🎯 Project Stats</h4>
        <ul style='list-style: none; padding: 0;'>
            <li>📊 <b>50+</b> Stores Analyzed</li>
            <li>📈 <b>1M+</b> Records Processed</li>
            <li>🎯 <b><15%</b> MAPE Achieved</li>
            <li>💰 <b>$XX,XXX</b> Annual Savings</li>
            <li>🤖 <b>4</b> Models Tested</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("<h4 style='color: white;'>⚡ Quick Actions</h4>", unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    if st.button("📥 Download Report", use_container_width=True):
        st.info("Report download coming soon!")
    
    if st.button("📧 Share Results", use_container_width=True):
        st.info("Share feature coming soon!")
    
    st.markdown("---")
    
    # Social links
    st.markdown("""
    <div style='color: white; text-align: center;'>
        <h4>🔗 Connect</h4>
        <a href='https://github.com/YOUR_USERNAME' target='_blank' style='color: white; text-decoration: none;'>
            💻 GitHub
        </a><br>
        <a href='https://linkedin.com/in/YOUR_PROFILE' target='_blank' style='color: white; text-decoration: none;'>
            💼 LinkedIn
        </a><br>
        <a href='mailto:your.email@example.com' style='color: white; text-decoration: none;'>
            📧 Email
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<p style='color: white; text-align: center; font-size: 0.8rem;'>Built with ❤️ by Shivam Gupta</p>", unsafe_allow_html=True)

# ============================================================================
# MAIN PAGE - HERO SECTION (FIXED CONTRAST)
# ============================================================================

# Animated title with better colors
st.markdown("""
<div class='animate-fade-in' style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-size: 3.5rem; margin-bottom: 15px;'>📦 Smart Supply Chain Forecasting</h1>
    <p style='font-size: 1.3rem; color: #4a5568; font-weight: 500;'>
       ML-Powered Demand Forecasting & Inventory Optimization
    </p>
    <p style='font-size: 1rem; color: #718096; margin-top: 10px;'>
        Achieving <span style='color: #667eea; font-weight: bold;'>72% improvement</span> through adaptive model selection
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# CUSTOM METRIC CARDS (ANIMATED)
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card animate-fade-in'>
        <div class='metric-value'>50+</div>
        <div class='metric-label'>🏪 Stores Analyzed</div>
        <div style='font-size: 0.8rem; margin-top: 10px;'>2 Store Segments</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card animate-fade-in' style='animation-delay: 0.1s;'>
        <div class='metric-value'>9.65%</div>
        <div class='metric-label'>🎯 Best MAPE</div>
        <div style='font-size: 0.8rem; margin-top: 10px;'>Store 1 - Naive</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card animate-fade-in' style='animation-delay: 0.2s;'>
        <div class='metric-value'>72%</div>
        <div class='metric-label'>📈 Improvement</div>
        <div style='font-size: 0.8rem; margin-top: 10px;'>Store 5 vs Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card animate-fade-in' style='animation-delay: 0.3s;'>
        <div class='metric-value'>$XX,XXX</div>
        <div class='metric-label'>💰 Annual Savings</div>
        <div style='font-size: 0.8rem; margin-top: 10px;'>Inventory Optimized</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# PROJECT HIGHLIGHTS - CARDS
# ============================================================================

st.markdown("## 🎯 Project Highlights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);'>
        <h3 style='color: white !important; margin-top: 0; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>📊 Store 1: Simple & Stable</h3>
        <ul style='line-height: 2; color: white; font-size: 1rem;'>
            <li><b>Complexity:</b> Low volatility, High autocorrelation (0.95)</li>
            <li><b>Best Model:</b> Naive Baseline</li>
            <li><b>MAPE:</b> <span style='color: #FFD700; font-weight: bold; font-size: 1.2rem;'>9.65%</span> ✅ (Excellent!)</li>
            <li><b>Insight:</b> Simple is best - ARIMA overfit at 17.28%</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);'>
        <h3 style='color: white !important; margin-top: 0; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>📈 Store 5: Complex & Volatile</h3>
        <ul style='line-height: 2; color: white; font-size: 1rem;'>
            <li><b>Complexity:</b> High volatility (CV: 37.74%), Low autocorr</li>
            <li><b>Best Model:</b> Prophet + Promotions</li>
            <li><b>MAPE:</b> <span style='color: #FFD700; font-weight: bold; font-size: 1.2rem;'>10.29%</span> ✅ (72% improvement!)</li>
            <li><b>Insight:</b> Advanced model needed - Naive failed at 36.97%</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# INTERACTIVE MODEL COMPARISON CHART - FIXED COLORS
# ============================================================================

st.markdown("## 📊 Interactive Model Performance")

# Create interactive comparison
model_data = pd.DataFrame({
    'Store': ['Store 1', 'Store 1', 'Store 5', 'Store 5', 'Store 5'],
    'Model': ['Naive', 'ARIMA', 'Naive', 'Prophet', 'Prophet + Promo'],
    'MAPE': [9.65, 17.28, 36.97, 20.39, 10.29],
    'Status': ['Best ✅', 'Overfit ❌', 'Poor ❌', 'Good ⚠️', 'Best ✅']
})

fig = px.bar(
    model_data,
    x='Model',
    y='MAPE',
    color='Store',
    text='MAPE',
    title='MAPE Comparison: Which Model Wins?',
    color_discrete_map={'Store 1': '#667eea', 'Store 5': '#f5576c'},
    height=500
)

# Add target line
fig.add_hline(
    y=15, 
    line_dash="dash", 
    line_color="green", 
    annotation_text="Target: <15% MAPE", 
    annotation_position="right",
    annotation=dict(font=dict(size=14, color="#1a1a2e"))
)

# Update text on bars
fig.update_traces(
    texttemplate='%{text:.2f}%', 
    textposition='outside',
    textfont=dict(size=14, color='#1a1a2e', family='Arial Black')
)

# FIX: Update layout with dark colors for axes
fig.update_layout(
    font=dict(size=14, color='#1a1a2e', family='Arial'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis_range=[0, 40],
    title=dict(
        text='MAPE Comparison: Which Model Wins?',
        font=dict(size=20, color='#1a1a2e', family='Arial Black'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=dict(
            text='Model',
            font=dict(size=16, color='#1a1a2e', family='Arial Black')
        ),
        tickfont=dict(size=14, color='#1a1a2e'),
        showgrid=False,
        showline=True,
        linewidth=2,
        linecolor='#cbd5e0'
    ),
    yaxis=dict(
        title=dict(
            text='MAPE (%)',
            font=dict(size=16, color='#1a1a2e', family='Arial Black')
        ),
        tickfont=dict(size=14, color='#1a1a2e'),
        gridcolor='#e2e8f0',
        showline=True,
        linewidth=2,
        linecolor='#cbd5e0'
    ),
    legend=dict(
        title=dict(
            text='Store',
            font=dict(size=14, color='#1a1a2e', family='Arial Black')
        ),
        font=dict(size=13, color='#1a1a2e'),
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='#cbd5e0',
        borderwidth=2
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial",
        font_color='#1a1a2e'
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# PROPHET IMPROVEMENT JOURNEY - FIXED COLORS
# ============================================================================

st.markdown("## 🚀 Prophet Model Evolution (Store 5)")

col1, col2 = st.columns([2, 1])

with col1:
    # Create journey chart
    journey_data = pd.DataFrame({
        'Stage': ['Naive\nBaseline', 'Prophet\nBaseline', 'Prophet\nTuned', 'Prophet +\nPromo'],
        'MAPE': [36.97, 20.39, 18.79, 10.29],
        'Color': ['#ff4444', '#ff9944', '#ffcc44', '#44ff44']
    })
    
    fig_journey = go.Figure()
    
    fig_journey.add_trace(go.Scatter(
        x=journey_data['Stage'],
        y=journey_data['MAPE'],
        mode='lines+markers+text',
        text=journey_data['MAPE'],
        texttemplate='%{text:.2f}%',
        textposition='top center',
        textfont=dict(size=16, color='#1a1a2e', family='Arial Black'),
        marker=dict(size=20, color=journey_data['Color'], line=dict(width=3, color='#1a1a2e')),
        line=dict(width=4, color='#667eea')
    ))
    
    # FIX: Update layout with dark colors
    fig_journey.update_layout(
        title=dict(
            text='From 36.97% to 10.29% MAPE: The Journey',
            font=dict(size=18, color='#1a1a2e', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text='Model Stage',
                font=dict(size=16, color='#1a1a2e', family='Arial Black')
            ),
            tickfont=dict(size=13, color='#1a1a2e'),
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='#cbd5e0'
        ),
        yaxis=dict(
            title=dict(
                text='MAPE (%)',
                font=dict(size=16, color='#1a1a2e', family='Arial Black')
            ),
            tickfont=dict(size=13, color='#1a1a2e'),
            range=[0, 40],
            gridcolor='#e2e8f0',
            showline=True,
            linewidth=2,
            linecolor='#cbd5e0'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        font=dict(color='#1a1a2e'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_color='#1a1a2e'
        )
    )
    
    st.plotly_chart(fig_journey, use_container_width=True)

with col2:
    st.markdown("""
    <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; height: 100%;'>
        <h4 style='color: #1a1a2e;'>📈 Improvement Breakdown</h4>
        <ul style='line-height: 2.5; color: #2d3748;'>
            <li><b>Stage 1 → 2:</b><br>↓ 16.58pp (44.9%)</li>
            <li><b>Stage 2 → 3:</b><br>↓ 1.60pp (7.8%)</li>
            <li><b>Stage 3 → 4:</b><br>↓ 8.50pp (45.2%)</li>
        </ul>
        <div style='background: #667eea; color: white; padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;'>
            <b>💡 Key Learning:</b><br>
            Feature engineering<br>(promotions) > Tuning
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# BUSINESS IMPACT SECTION
# ============================================================================

st.markdown("## 💰 Business Impact & ROI")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center;'>
        <h3 style='color: white;'>📦 Inventory</h3>
        <div style='font-size: 2rem; font-weight: bold; margin: 15px 0;'>$XX,XXX</div>
        <p>Annual Cost Savings<br>via EOQ Optimization</p>
        <div style='background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px; margin-top: 15px;'>
            95% Service Level Maintained
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center;'>
        <h3 style='color: white;'>📊 Forecast</h3>
        <div style='font-size: 2rem; font-weight: bold; margin: 15px 0;'>72%</div>
        <p>Accuracy Improvement<br>on Complex Stores</p>
        <div style='background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px; margin-top: 15px;'>
            From 36.97% to 10.29% MAPE
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center;'>
        <h3 style='color: white;'>🎯 Scalability</h3>
        <div style='font-size: 2rem; font-weight: bold; margin: 15px 0;'>1,115</div>
        <p>Total Stores<br>Ready for Deployment</p>
        <div style='background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px; margin-top: 15px;'>
            Framework Validated ✅
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# KEY INSIGHTS WITH ICONS
# ============================================================================

st.markdown("## 💡 Key Insights & Learnings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: #d1fae5; border-left: 5px solid #10b981; padding: 20px; border-radius: 10px;'>
        <h4 style='color: #065f46; margin-top: 0;'>✅ What Worked:</h4>
        <ul style='color: #047857; line-height: 2;'>
            <li><b>🎯 Store Segmentation:</b> Data-driven model selection beats one-size-fits-all</li>
            <li><b>🔍 Feature Engineering:</b> Adding promotions → 10pp MAPE improvement</li>
            <li><b>📊 Baseline Comparison:</b> Prevented deploying worse models (ARIMA on Store 1)</li>
            <li><b>🎨 Domain Knowledge:</b> Understanding business context > Pure statistics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #fef3c7; border-left: 5px solid #f59e0b; padding: 20px; border-radius: 10px;'>
        <h4 style='color: #92400e; margin-top: 0;'>⚠️ Challenges & Solutions:</h4>
        <ul style='color: #b45309; line-height: 2;'>
            <li><b>High Volatility (Store 5):</b> Solved with Prophet's flexible changepoints</li>
            <li><b>ARIMA Failures:</b> Learned when NOT to use complex models</li>
            <li><b>Overfitting Risk:</b> Naive beat ARIMA on simple store (9.65% vs 17.28%)</li>
            <li><b>Promotion Impact:</b> Required external regressor, not just historical data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# NEXT STEPS & CTA
# ============================================================================

st.markdown("## 🚀 Explore the Dashboard")

st.markdown("""
<div style='background: #eff6ff; border-left: 5px solid #3b82f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h4 style='color: #1e40af; margin-top: 0;'>📌 Navigate to other pages using the sidebar:</h4>
    <ul style='color: #1e3a8a; line-height: 2;'>
        <li><b>📊 Executive Summary:</b> Comprehensive project overview with visualizations</li>
        <li><b>📈 Demand Forecasting:</b> Interactive store-level forecasts with Prophet</li>
        <li><b>📦 Inventory Optimizer:</b> Real-time EOQ calculator with cost analysis</li>
        <li><b>🎯 Model Performance:</b> Detailed model comparison and diagnostics</li>
    </ul>
</div>
""", unsafe_allow_html=True)



st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class='footer'>
    <p style='font-size: 1.2rem;'><b>Smart Supply Chain Forecasting Dashboard</b></p>
    <p style='font-size: 0.95rem;'>Built with Python • Prophet • Streamlit | © 2024 Shivam Gupta</p>
    <p style='margin-top: 15px;'>
        <a href='https://github.com/YOUR_USERNAME' target='_blank'>GitHub</a> •
        <a href='https://linkedin.com/in/YOUR_PROFILE' target='_blank'>LinkedIn</a> •
        <a href='mailto:your.email@example.com'>Email</a>
    </p>
    <p style='font-size: 0.8rem; color: #999; margin-top: 10px;'>
        Last Updated: December 18, 2024 | Version 1.0
    </p>
</div>
""", unsafe_allow_html=True)
