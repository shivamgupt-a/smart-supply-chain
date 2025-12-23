# ============================================================================
# INVENTORY OPTIMIZER PAGE
# EOQ, safety stock, and scenarios
# Author: Shivam Gupta
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(page_title="Inventory Optimizer", page_icon="📦", layout="wide")

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

st.title("📦 Inventory Optimization")
st.markdown("""
<p style='text-align:center; font-size:1.0rem; color:#4a5568;'>
Compute EOQ, safety stock, and reorder points, and see the cost impact of better forecasts.
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR-LIKE CONTROLS (TOP)
# ============================================================================

col_sel, col_scen = st.columns([2, 2])
with col_sel:
    store_choice = st.selectbox(
        "Select store:",
        ["Store 1 (Simple)", "Store 5 (Complex)"]
    )
with col_scen:
    scenario = st.selectbox(
        "Scenario:",
        ["Base Case", "High Fuel Cost (Order Cost ↑)", "Expensive Warehouse (Holding Cost ↑)"]
    )

store_num = 1 if "Store 1" in store_choice else 5

# Base parameters
unit_cost = 50
order_cost = 150
holding_cost_percent = 0.25
working_days = 365
lead_time_days = st.slider("Lead time (days):", 3, 21, 7, step=1)
service_level = st.slider("Service level (%):", 85, 99, 95, step=1) / 100

if scenario == "High Fuel Cost (Order Cost ↑)":
    order_cost *= 1.5
elif scenario == "Expensive Warehouse (Holding Cost ↑)":
    holding_cost_percent *= 1.5

holding_cost_per_unit = unit_cost * holding_cost_percent

# ============================================================================
# LOAD DEMAND STATS
# ============================================================================

@st.cache_data
def load_demand_stats(store_num: int):
    path = f"C:/Users/Shivam Gupta/Coding/smart-supply-chain/data/processed/store_{store_num}_data.csv"
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df[df['Open'] == 1].copy()

    mean_daily = df['Sales'].mean()
    std_daily = df['Sales'].std()
    annual_demand = mean_daily * working_days
    cv = (std_daily / mean_daily) * 100

    return {
        'mean_daily_demand': mean_daily,
        'std_daily_demand': std_daily,
        'annual_demand': annual_demand,
        'cv': cv
    }

stats_store = load_demand_stats(store_num)

# ============================================================================
# EOQ + COSTS
# ============================================================================

def total_inventory_cost(Q, D, S, H):
    return (D / Q) * S + (Q / 2) * H

D = stats_store['annual_demand']
S = order_cost
H = holding_cost_per_unit

eoq = np.sqrt((2 * D * S) / H)
orders_per_year = D / eoq
days_between_orders = 365 / orders_per_year

# naive policy: weekly order with 20% buffer
naive_Q = stats_store['mean_daily_demand'] * 7 * 1.2
naive_cost = total_inventory_cost(naive_Q, D, S, H)
eoq_cost = total_inventory_cost(eoq, D, S, H)

annual_savings = naive_cost - eoq_cost
savings_pct = (annual_savings / naive_cost) * 100

# =========================================================================#
# DEMAND STATS + KPIs
# =========================================================================#

st.subheader(f"🏪 {store_choice} - Demand & Policy Summary")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{stats_store['mean_daily_demand']:.0f}</div>
      <div class='metric-label'>Mean Daily Demand</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{stats_store['std_daily_demand']:.0f}</div>
      <div class='metric-label'>Std Dev (Daily)</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{stats_store['cv']:.1f}%</div>
      <div class='metric-label'>Coeff. of Variation</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{D:.0f}</div>
      <div class='metric-label'>Annual Demand</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("✅ Optimized EOQ Policy")
    st.markdown(f"""
    **Economic Order Quantity (EOQ):** `{eoq:.0f}` units  
    **Orders per year:** `{orders_per_year:.1f}`  
    **Days between orders:** `{days_between_orders:.1f}` days  

    **Optimized annual cost:** `${eoq_cost:,.2f}`  
    """)

with col_right:
    st.subheader("❌ Current Weekly Policy")
    st.markdown(f"""
    **Naive order quantity:** `{naive_Q:.0f}` units  
    **Orders per year:** `{D / naive_Q:.1f}`  
    **Days between orders:** `{365 / (D / naive_Q):.1f}` days  

    **Current annual cost:** `${naive_cost:,.2f}`  
    """)

st.markdown("---")

# ============================================================================
# COST SAVINGS + BADGE
# ============================================================================

st.subheader("💰 Cost Savings")

badge_color = "#22c55e" if savings_pct > 25 else "#f97316" if savings_pct > 10 else "#ef4444"
badge_label = "Excellent" if savings_pct > 25 else "Good" if savings_pct > 10 else "Low"

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>${annual_savings:,.0f}</div>
      <div class='metric-label'>Annual Savings</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{savings_pct:.1f}%</div>
      <div class='metric-label'>Cost Reduction</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div style='background:{badge_color};padding:18px;border-radius:15px;color:white;
                text-align:center;box-shadow:0 5px 15px rgba(0,0,0,0.2);margin:10px 0;'>
        <div style='font-size:2.0rem;font-weight:bold;'>{badge_label}</div>
        <div style='font-size:0.9rem;margin-top:5px;'>Savings Quality</div>
    </div>
    """, unsafe_allow_html=True)

# Cost bar chart
fig_cost = go.Figure()
fig_cost.add_trace(go.Bar(
    x=['Current'], y=[naive_cost],
    name='Current Policy', marker_color='coral',
    text=[f"${naive_cost:,.0f}"], textposition='outside'
))
fig_cost.add_trace(go.Bar(
    x=['Optimized'], y=[eoq_cost],
    name='Optimized EOQ', marker_color='lightgreen',
    text=[f"${eoq_cost:,.0f}"], textposition='outside'
))

fig_cost.update_layout(
    title=dict(text='Annual Inventory Cost Comparison', font=dict(size=17, color='#1a1a2e', family='Arial Black'), x=0.5),
    xaxis=dict(title='', tickfont=dict(color='#1a1a2e')),
    yaxis=dict(title='Cost ($)', tickfont=dict(color='#1a1a2e'),
               gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
    plot_bgcolor='white', paper_bgcolor='white', height=380,
    legend=dict(font=dict(color='#1a1a2e'), bgcolor='rgba(255,255,255,0.9)', bordercolor='#cbd5e0')
)
st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("---")

# ============================================================================
# SAFETY STOCK & REORDER POINT
# ============================================================================

st.subheader("🎯 Safety Stock & Reorder Point")

z = stats.norm.ppf(service_level)
safety_stock = z * stats_store['std_daily_demand'] * np.sqrt(lead_time_days)
reorder_point = stats_store['mean_daily_demand'] * lead_time_days + safety_stock

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    **Safety stock:** `{safety_stock:.0f}` units  

    Formula: `Z × σ × √Lead_Time`  
    - Z ({service_level*100:.0f}%): `{z:.2f}`  
    - σ (daily): `{stats_store['std_daily_demand']:.0f}`  
    - Lead time: `{lead_time_days}` days  
    """)
with c2:
    st.markdown(f"""
    **Reorder point:** `{reorder_point:.0f}` units  

    Formula: `Demand_during_lead_time + Safety_stock`  
    - Demand during lead time: `{stats_store['mean_daily_demand'] * lead_time_days:.0f}`  
    - Safety stock: `{safety_stock:.0f}`  
    """)

st.markdown("---")

# ============================================================================
# EOQ COST CURVE
# ============================================================================

st.subheader("📈 EOQ Cost Curve & Near-Optimal Zone")

Q_range = np.linspace(eoq * 0.3, eoq * 2, 100)
ordering_costs = (D / Q_range) * S
holding_costs = (Q_range / 2) * H
total_costs = ordering_costs + holding_costs

fig_curve = go.Figure()
fig_curve.add_trace(go.Scatter(
    x=Q_range, y=ordering_costs,
    mode='lines', name='Ordering Cost', line=dict(color='red', width=2)
))
fig_curve.add_trace(go.Scatter(
    x=Q_range, y=holding_costs,
    mode='lines', name='Holding Cost', line=dict(color='blue', width=2)
))
fig_curve.add_trace(go.Scatter(
    x=Q_range, y=total_costs,
    mode='lines', name='Total Cost', line=dict(color='green', width=3, dash='dash')
))

# Near optimal band
low_band, high_band = eoq * 0.8, eoq * 1.2
fig_curve.add_vrect(
    x0=low_band, x1=high_band,
    fillcolor="rgba(129, 140, 248, 0.15)", line_width=0,
    annotation_text="Near-optimal zone", annotation_position="top left"
)

fig_curve.add_trace(go.Scatter(
    x=[eoq], y=[eoq_cost],
    mode='markers', name=f'EOQ ({eoq:.0f})',
    marker=dict(size=14, color='gold', line=dict(width=2, color='#1a1a2e'))
))

fig_curve.update_layout(
    title=dict(text='EOQ Cost Curve', font=dict(size=17, color='#1a1a2e', family='Arial Black'), x=0.5),
    xaxis=dict(title='Order Quantity (Q)', tickfont=dict(color='#1a1a2e'),
               showline=True, linewidth=2, linecolor='#cbd5e0'),
    yaxis=dict(title='Annual Cost ($)', tickfont=dict(color='#1a1a2e'),
               gridcolor='#e2e8f0', showline=True, linewidth=2, linecolor='#cbd5e0'),
    plot_bgcolor='white', paper_bgcolor='white', height=430,
    legend=dict(font=dict(color='#1a1a2e'), bgcolor='rgba(255,255,255,0.9)')
)
st.plotly_chart(fig_curve, use_container_width=True)

st.info("""
**Interpretation:**
- Ordering cost decreases as Q increases (fewer orders).
- Holding cost increases as Q increases (more inventory).
- Total cost is U-shaped with minimum at EOQ.
- The shaded band shows a **near-optimal region** around EOQ.
""")

st.markdown("---")

# ============================================================================
# POLICY TABLE + DOWNLOAD
# ============================================================================

st.subheader("📋 Inventory Policy Summary")

policy_df = pd.DataFrame({
    'Parameter': [
        'Store',
        'Scenario',
        'EOQ (units)',
        'Reorder Point (units)',
        'Safety Stock (units)',
        'Orders Per Year',
        'Days Between Orders',
        'Service Level',
        'Lead Time (days)',
        'Current Annual Cost',
        'Optimized Annual Cost',
        'Annual Savings',
        'Savings Percent'
    ],
    'Value': [
        store_choice,
        scenario,
        f"{eoq:.0f}",
        f"{reorder_point:.0f}",
        f"{safety_stock:.0f}",
        f"{orders_per_year:.1f}",
        f"{days_between_orders:.1f}",
        f"{service_level*100:.0f}%",
        f"{lead_time_days}",
        f"${naive_cost:,.2f}",
        f"${eoq_cost:,.2f}",
        f"${annual_savings:,.2f}",
        f"{savings_pct:.1f}%"
    ]
})
st.dataframe(policy_df, use_container_width=True)

csv_policy = policy_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download Policy CSV",
    data=csv_policy,
    file_name=f'inventory_policy_store{store_num}.csv',
    mime='text/csv'
)

st.markdown("---")

st.subheader("💡 How to Explain This Page in an Interview")
st.info("""
- Forecasts are not just for accuracy; they drive **inventory decisions**.
- EOQ and safety stock ensure we **minimize cost** while hitting a **95% service level**.
- Scenario analysis (fuel cost, warehouse cost) shows you can adapt to business shocks.
""")
