# ═══════════════════════════════════════════════════
# BANK CHURN ANALYTICS DASHBOARD
# Student: Dhananjay Singh | Unified Mentor
# ═══════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG — Must be first ──
st.set_page_config(
    page_title="Bank Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS — Dark Theme ──
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* KPI Glass Card */
    .kpi-card {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(43, 142, 255, 0.4);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(43, 142, 255, 0.1);
    min-height: 140px;
}
    .kpi-value {
    font-size: 24px;
    font-weight: 700;
    color: #2B8EFF;
    margin: 8px 0;
    white-space: nowrap;
}
    .kpi-label {
        font-size: 13px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-delta {
        font-size: 12px;
        color: #F0B429;
        margin-top: 4px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161B22;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8B949E;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #2B8EFF;
        color: white;
        border-radius: 8px;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ──
@st.cache_data
def load_data():
    df = pd.read_csv(r'D:\Python project\data\European_Bank_Segmented.csv')
    return df

@st.cache_data
def load_risk_scores():
    risk_df = pd.read_csv(r'D:\Python project\data\Customer_Risk_Scores.csv')
    return risk_df

# Load data
df = load_data()
risk_df = load_risk_scores()

# ── SIDEBAR FILTERS ──
st.sidebar.image("https://img.icons8.com/fluency/96/bank.png", width=60)
st.sidebar.title("🏦 BankChurn Analytics")
st.sidebar.markdown("---")

st.sidebar.subheader("📊 Filters")

# Geography filter
geography = st.sidebar.multiselect(
    "Geography",
    options=df['Geography'].unique(),
    default=df['Geography'].unique()
)

# Gender filter
gender = st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Age Group filter
age_group = st.sidebar.multiselect(
    "Age Group",
    options=df['AgeGroup'].unique(),
    default=df['AgeGroup'].unique()
)

st.sidebar.markdown("---")
st.sidebar.caption("Unified Mentor | Finance Analytics")
st.sidebar.caption("Student: Dhananjay Singh")

# ── APPLY FILTERS ──
df_filtered = df[
    (df['Geography'].isin(geography)) &
    (df['Gender'].isin(gender)) &
    (df['AgeGroup'].isin(age_group))
]

# ── TABS ──
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Geography",
    "Demographics",
    "High Value Customers",
    "Churn Predictor",
    "Retention ROI Simulator"
])

# ── TAB 1: OVERVIEW ──
with tab1:
    st.title("Customer Churn Analytics Dashboard")
    st.caption("European Banking | Unified Mentor Finance Analytics Project")
    st.markdown("---")
    
    # ── KPI CALCULATIONS ──
    total_customers = len(df_filtered)
    churned_customers = df_filtered['Exited'].sum()
    churn_rate = df_filtered['Exited'].mean() * 100
    revenue_at_risk = df_filtered[df_filtered['Exited']==1]['Balance'].sum()
    germany_churn = df_filtered[df_filtered['Geography']=='Germany']['Exited'].mean() * 100

    # ── KPI CARDS ──
    k1, k2, k3, k4, k5 = st.columns([1, 1, 1, 1.3, 1])

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-delta">Full Portfolio</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Churned Customers</div>
            <div class="kpi-value">{int(churned_customers):,}</div>
            <div class="kpi-delta">Customers Lost</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Churn Rate</div>
            <div class="kpi-value">{churn_rate:.1f}%</div>
            <div class="kpi-delta">vs 15% Benchmark</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Revenue at Risk</div>
            <div class="kpi-value">€{revenue_at_risk/1e6:.1f}M</div>
            <div class="kpi-delta">Lost Balance</div>
        </div>""", unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Germany Churn</div>
            <div class="kpi-value">{germany_churn:.1f}%</div>
            <div class="kpi-delta">Highest Risk Region</div>
        </div>""", unsafe_allow_html=True)
        
# ── OVERVIEW CHART ──
    st.markdown("###")
    col_left, col_right = st.columns(2)

    with col_left:
        # Churn by Geography bar chart
        geo_churn = df_filtered.groupby('Geography').agg(
            Churn_Rate=('Exited', 'mean'),
            Total=('Exited', 'count'),
            Churned=('Exited', 'sum')
        ).reset_index()
        geo_churn['Churn_Rate'] = (geo_churn['Churn_Rate'] * 100).round(2)
        geo_churn['Retained'] = geo_churn['Total'] - geo_churn['Churned']

        fig_geo = px.bar(
            geo_churn,
            x='Geography',
            y=['Churned', 'Retained'],
            title='Churned vs Retained by Geography',
            color_discrete_map={
                'Churned': '#e74c3c',
                'Retained': '#2ecc71'
            },
            barmode='group',
            template='plotly_dark'
        )
        fig_geo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend_title='Status',
            xaxis_title='Geography',
            yaxis_title='Number of Customers'
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        st.caption("Germany shows highest churn volume despite smaller customer base")

    with col_right:
        # Churn rate donut
        churn_counts = df_filtered['Exited'].value_counts()
        fig_donut = px.pie(
            values=churn_counts.values,
            names=['Retained', 'Churned'],
            title='Overall Churn Distribution',
            hole=0.6,
            color_discrete_sequence=['#2ecc71', '#e74c3c'],
            template='plotly_dark'
        )
        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.caption("20.37% overall churn — 5.37 points above European benchmark")        