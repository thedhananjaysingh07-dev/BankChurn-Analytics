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


# ── TAB 2: GEOGRAPHY ──
with tab2:
    st.title("Geography Analysis")
    st.caption("Churn patterns across France, Germany and Spain")
    st.markdown("---")

    # ── ROW 1: Two charts side by side ──
    col1, col2 = st.columns(2)

    with col1:
        # Churn rate by Geography
        geo_rate = df_filtered.groupby('Geography')['Exited'].mean()\
                   .reset_index()
        geo_rate['Churn_Rate'] = (geo_rate['Exited'] * 100).round(2)
        geo_rate = geo_rate.sort_values('Churn_Rate', ascending=True)

        fig_geo_rate = px.bar(
            geo_rate,
            x='Churn_Rate',
            y='Geography',
            orientation='h',
            title='Churn Rate by Country',
            color='Churn_Rate',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_geo_rate.update_traces(
    texttemplate='%{x:.1f}%',
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Churn Rate: %{x:.1f}%<extra></extra>'
)
        fig_geo_rate.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_geo_rate, use_container_width=True)
        st.caption("Germany churn rate (32.4%) is double France and Spain (~16%)")

    with col2:
        # Retained vs Churned stacked bar
        geo_counts = df_filtered.groupby('Geography').agg(
            Churned=('Exited', 'sum'),
            Total=('Exited', 'count')
        ).reset_index()
        geo_counts['Retained'] = geo_counts['Total'] - geo_counts['Churned']

        fig_stacked = px.bar(
            geo_counts,
            x='Geography',
            y=['Retained', 'Churned'],
            title='Retained vs Churned by Country',
            color_discrete_map={
                'Retained': '#2ecc71',
                'Churned': '#e74c3c'
            },
            barmode='stack',
            template='plotly_dark'
        )
        fig_stacked.update_traces(
    hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:,}<extra></extra>'
)
        fig_stacked.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        st.caption("France has largest customer base but lowest churn rate")

    # ── ROW 2: Two charts side by side ──
    col3, col4 = st.columns(2)

    with col3:
        # Gender x Geography churn
        gender_geo = df_filtered.groupby(
            ['Geography', 'Gender'])['Exited'].mean()\
            .reset_index()
        gender_geo['Churn_Rate'] = (gender_geo['Exited'] * 100).round(2)

        fig_gender_geo = px.bar(
            gender_geo,
            x='Geography',
            y='Churn_Rate',
            color='Gender',
            barmode='group',
            title='Churn Rate by Geography and Gender',
            color_discrete_map={
                'Female': '#e74c3c',
                'Male': '#3498db'
            },
            template='plotly_dark'
        )
        fig_gender_geo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_gender_geo.update_traces(
    hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:.1f}%<extra></extra>'
)
        st.plotly_chart(fig_gender_geo, use_container_width=True)
        st.caption("Germany Female churn at 37.55% — highest gender-country combination")

    with col4:
        # Geography x Age heatmap
        heat_data = df_filtered.pivot_table(
            values='Exited',
            index='AgeGroup',
            columns='Geography',
            aggfunc='mean'
        ) * 100

        # Order age groups correctly
        age_order = ['<30', '30-45', '46-60', '60+']
        heat_data = heat_data.reindex(age_order)

        fig_heat = px.imshow(
            heat_data,
            title='Churn Rate % — Geography × Age Group',
            color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'],
            aspect='auto',
            text_auto='.1f',
            template='plotly_dark'
        )
        fig_heat.update_traces(
    hovertemplate='Age: %{y}<br>Country: %{x}<br>Churn Rate: %{z:.1f}%<extra></extra>'
)
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("Germany + Age 46-60 = 67.33% — most extreme segment in dataset")        
        
        
# ── TAB 3: DEMOGRAPHICS ──
with tab3:
    st.title("Demographics Analysis")
    st.caption("Churn patterns across age groups, gender and engagement status")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        # Churn by Age Group
        age_order = ['<30', '30-45', '46-60', '60+']
        age_churn = df_filtered.groupby('AgeGroup')['Exited'].mean()\
                    .reset_index()
        age_churn['Churn_Rate'] = (age_churn['Exited'] * 100).round(2)
        age_churn['AgeGroup'] = pd.Categorical(
            age_churn['AgeGroup'], categories=age_order, ordered=True)
        age_churn = age_churn.sort_values('AgeGroup')

        fig_age = px.bar(
            age_churn,
            x='AgeGroup',
            y='Churn_Rate',
            title='Churn Rate by Age Group',
            color='Churn_Rate',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_age.update_traces(texttemplate='%{text:.1f}%',
                              textposition='outside')
        fig_age.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            yaxis_title='Churn Rate %'
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.caption("Age 46-60 churns at 51.12% — highest of any age group")

    with col2:
        # Churn by Gender
        gender_churn = df_filtered.groupby('Gender')['Exited'].mean()\
                       .reset_index()
        gender_churn['Churn_Rate'] = (gender_churn['Exited'] * 100).round(2)

        fig_gender = px.bar(
            gender_churn,
            x='Gender',
            y='Churn_Rate',
            title='Churn Rate by Gender',
            color='Gender',
            color_discrete_map={
                'Female': '#e74c3c',
                'Male': '#3498db'
            },
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_gender.update_traces(texttemplate='%{text:.1f}%',
                                 textposition='outside')
        fig_gender.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title='Churn Rate %',
            showlegend=False
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        st.caption("Female churn (25.07%) is 8.61 points higher than Male (16.46%)")

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        # Active vs Inactive
        active_churn = df_filtered.groupby('IsActiveMember')['Exited'].mean()\
                       .reset_index()
        active_churn['Status'] = active_churn['IsActiveMember'].map(
            {0: 'Inactive', 1: 'Active'})
        active_churn['Churn_Rate'] = (active_churn['Exited'] * 100).round(2)

        fig_active = px.bar(
            active_churn,
            x='Status',
            y='Churn_Rate',
            title='Churn Rate by Engagement Status',
            color='Status',
            color_discrete_map={
                'Active': '#2ecc71',
                'Inactive': '#e74c3c'
            },
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_active.update_traces(texttemplate='%{text:.1f}%',
                                 textposition='outside')
        fig_active.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title='Churn Rate %',
            showlegend=False
        )
        st.plotly_chart(fig_active, use_container_width=True)
        st.caption("Inactive members churn at 26.85% vs 14.27% for active — engagement is key")

    with col4:
        # NumOfProducts churn
        prod_churn = df_filtered.groupby('NumOfProducts')['Exited'].mean()\
                     .reset_index()
        prod_churn['Churn_Rate'] = (prod_churn['Exited'] * 100).round(2)

        fig_prod = px.bar(
            prod_churn,
            x='NumOfProducts',
            y='Churn_Rate',
            title='Churn Rate by Number of Products',
            color='Churn_Rate',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_prod.update_traces(texttemplate='%{text:.1f}%',
                               textposition='outside')
        fig_prod.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_showscale=False,
    xaxis_title='Number of Products',
    yaxis_title='Churn Rate %',
    xaxis=dict(tickmode='linear', tick0=1, dtick=1)
)
        st.plotly_chart(fig_prod, use_container_width=True)
        st.caption("U-shaped pattern: 2 products safest (7.6%), 4 products = 100% churn")
        
        
        # ── TAB 4: HIGH VALUE CUSTOMERS ──
with tab4:
    st.title("High Value Customer Analysis")
    st.caption("Churn risk among premium and high CLV segments")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        # Churn by CLV Segment
        clv_churn = df_filtered.groupby('CLV_Segment').agg(
            Churn_Rate=('Exited', 'mean'),
            Customers=('Exited', 'count'),
            Revenue_Lost=('Balance', lambda x: x[df_filtered.loc[x.index, 'Exited']==1].sum())
        ).reset_index()
        clv_churn['Churn_Rate'] = (clv_churn['Churn_Rate'] * 100).round(2)
        clv_churn['Revenue_Lost_M'] = (clv_churn['Revenue_Lost'] / 1e6).round(1)

        fig_clv = px.bar(
            clv_churn,
            x='CLV_Segment',
            y='Churn_Rate',
            title='Churn Rate by CLV Segment',
            color='Churn_Rate',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_clv.update_traces(texttemplate='%{text:.1f}%',
                              textposition='outside')
        fig_clv.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            yaxis_title='Churn Rate %'
        )
        st.plotly_chart(fig_clv, use_container_width=True)
        st.caption("Premium CLV churn at 24.20% — highest value customers are leaving")

    with col2:
        # Revenue lost by CLV segment
        fig_rev = px.bar(
            clv_churn,
            x='CLV_Segment',
            y='Revenue_Lost_M',
            title='Revenue Lost by CLV Segment (€M)',
            color='Revenue_Lost_M',
            color_continuous_scale=['#f39c12', '#e74c3c'],
            template='plotly_dark',
            text='Revenue_Lost_M'
        )
        fig_rev.update_traces(texttemplate='€%{text:.1f}M',
                              textposition='outside')
        fig_rev.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            yaxis_title='Revenue Lost (€M)'
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        st.caption("83% of €185.5M revenue risk concentrated in High + Premium segments")

    col3, col4 = st.columns(2)

    with col3:
        # Persona churn rates
        persona_churn = df_filtered.groupby('Persona')['Exited'].mean()\
                        .reset_index()
        persona_churn['Churn_Rate'] = (persona_churn['Exited'] * 100).round(2)
        persona_churn = persona_churn.sort_values('Churn_Rate', ascending=True)

        fig_persona = px.bar(
            persona_churn,
            x='Churn_Rate',
            y='Persona',
            orientation='h',
            title='Churn Rate by Customer Persona',
            color='Churn_Rate',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            template='plotly_dark',
            text='Churn_Rate'
        )
        fig_persona.update_traces(texttemplate='%{text:.1f}%',
                                  textposition='outside')
        fig_persona.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            xaxis_title='Churn Rate %'
        )
        st.plotly_chart(fig_persona, use_container_width=True)
        st.caption("At-Risk Premium persona churns at 31.18% — same balance as Active Saver (16%)")

    with col4:
        # Balance distribution churned vs retained
        fig_box = px.box(
            df_filtered,
            x='Exited',
            y='Balance',
            title='Balance Distribution — Churned vs Retained',
            color='Exited',
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            template='plotly_dark',
            labels={'Exited': 'Status', 'Balance': 'Account Balance (€)'}
        )
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickvals=[0,1], ticktext=['Retained','Churned']),
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.caption("Churned customers hold higher median balance — financial disengagement, not poverty")        