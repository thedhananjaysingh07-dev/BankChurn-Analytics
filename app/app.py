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

    # FIX 4: Germany churn safety check — handle NaN when Germany filtered out
    germany_data = df_filtered[df_filtered['Geography']=='Germany']['Exited']
    if len(germany_data) > 0:
        germany_churn = germany_data.mean() * 100
        germany_display = f"{germany_churn:.1f}%"
    else:
        germany_churn = 0
        germany_display = "N/A"

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
            <div class="kpi-value">{germany_display}</div>
            <div class="kpi-delta">Highest Risk Region</div>
        </div>""", unsafe_allow_html=True)

    # FIX 1: Insight callout boxes
    st.markdown("###")
    i1, i2, i3 = st.columns(3)

    with i1:
        st.markdown("""
        <div style="background:rgba(231,76,60,0.1); border-left:4px solid #e74c3c;
                    border-radius:8px; padding:16px; margin:8px 0;">
            <div style="font-size:11px; color:#e74c3c; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px;">
                Critical Finding</div>
            <div style="font-size:14px; color:#FAFAFA; margin-top:6px;">
                Age 46-60 churns at <b>51.12%</b> — rejecting our hypothesis
                that older customers are more loyal.</div>
        </div>""", unsafe_allow_html=True)

    with i2:
        st.markdown("""
        <div style="background:rgba(240,180,41,0.1); border-left:4px solid #F0B429;
                    border-radius:8px; padding:16px; margin:8px 0;">
            <div style="font-size:11px; color:#F0B429; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px;">
                Key Insight</div>
            <div style="font-size:14px; color:#FAFAFA; margin-top:6px;">
                Clusters 0 & 3 hold identical balance (~€122K) but churn at
                <b>16% vs 31%</b> — engagement alone explains the gap.</div>
        </div>""", unsafe_allow_html=True)

    with i3:
        st.markdown("""
        <div style="background:rgba(43,142,255,0.1); border-left:4px solid #2B8EFF;
                    border-radius:8px; padding:16px; margin:8px 0;">
            <div style="font-size:11px; color:#2B8EFF; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px;">
                Benchmark</div>
            <div style="font-size:14px; color:#FAFAFA; margin-top:6px;">
                Our churn rate of <b>20.37%</b> is 5.37 points above the
                European banking benchmark of 15% (PwC 2025).</div>
        </div>""", unsafe_allow_html=True)

    # ── OVERVIEW CHART ──
    st.markdown("###")
    col_left, col_right = st.columns(2)

    with col_left:
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

    col1, col2 = st.columns(2)

    with col1:
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
            textposition='outside'
        )
        fig_geo_rate.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_geo_rate, use_container_width=True)
        st.caption("Germany churn rate (32.4%) is double France and Spain (~16%)")

    with col2:
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
        fig_stacked.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        st.caption("France has largest customer base but lowest churn rate")

    col3, col4 = st.columns(2)

    with col3:
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
        st.plotly_chart(fig_gender_geo, use_container_width=True)
        st.caption("Germany Female churn at 37.55% — highest gender-country combination")

    with col4:
        heat_data = df_filtered.pivot_table(
            values='Exited',
            index='AgeGroup',
            columns='Geography',
            aggfunc='mean'
        ) * 100

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

    col3, col4 = st.columns(2)

    with col3:
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


# ── TAB 5: CHURN PREDICTOR ──
with tab5:
    st.title("Churn Predictor")
    st.caption("Live ML model — Random Forest | AUC 0.851 | Recall 64%")
    st.markdown("---")

    # ── SECTION 1: Risk Score Explorer ──
    st.subheader("Customer Risk Score Explorer")

    risk_tier_filter = st.selectbox(
        "Filter by Risk Tier",
        options=['All', 'Critical Risk', 'High Risk',
                 'Medium Risk', 'Low Risk']
    )

    if risk_tier_filter == 'All':
        display_risk = risk_df
    else:
        display_risk = risk_df[risk_df['Risk_Tier'] == risk_tier_filter]

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        critical = len(risk_df[risk_df['Risk_Tier']=='Critical Risk'])
        st.metric("Critical Risk", critical, "73.7% actual churn")
    with r2:
        high = len(risk_df[risk_df['Risk_Tier']=='High Risk'])
        st.metric("High Risk", high, "41.8% actual churn")
    with r3:
        medium = len(risk_df[risk_df['Risk_Tier']=='Medium Risk'])
        st.metric("Medium Risk", medium, "18.8% actual churn")
    with r4:
        low = len(risk_df[risk_df['Risk_Tier']=='Low Risk'])
        st.metric("Low Risk", low, "6.1% actual churn")

    st.dataframe(
        display_risk[['Churn_Probability', 'Risk_Tier',
                      'Actual_Churn', 'Age', 'Balance',
                      'IsActiveMember', 'Geography_Germany',
                      'Geography_France', 'Geography_Spain']]\
        .sort_values('Churn_Probability', ascending=False)\
        .head(50),
        use_container_width=True
    )

    st.markdown("---")

    # ── SECTION 2: Individual Predictor ──
    st.subheader("Individual Customer Churn Predictor")
    st.caption("Input customer details to get instant churn probability")

    import pickle

    @st.cache_resource
    def load_model():
        with open(r'D:\Python project\models\rf_model.pkl', 'rb') as f:
            return pickle.load(f)

    model = load_model()

    col1, col2, col3 = st.columns(3)

    with col1:
        pred_age = st.slider("Age", 18, 92, 40)
        pred_balance = st.number_input("Account Balance (€)", 0, 300000, 50000)
        pred_credit_score = st.slider("Credit Score", 350, 850, 650)
        pred_estimated_salary = st.number_input("Estimated Salary (€)",
                                                 0, 200000, 80000)
        pred_tenure = st.slider("Tenure (Years)", 0, 10, 5)

    with col2:
        # FIX 3: Renamed to pred_* to avoid conflict with sidebar filters
        pred_num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
        pred_has_cr_card = st.selectbox("Has Credit Card", [1, 0],
                                         format_func=lambda x: "Yes" if x==1 else "No")
        pred_is_active = st.selectbox("Is Active Member", [1, 0],
                                       format_func=lambda x: "Yes" if x==1 else "No")
        pred_geography = st.selectbox("Geography",
                                       ["France", "Germany", "Spain"])
        pred_gender = st.selectbox("Gender", ["Male", "Female"])

    with col3:
        pred_clv_score = (pred_balance * 0.5) + (pred_estimated_salary * 0.3) + (pred_tenure * 1000 * 0.2)
        pred_engagement = pred_is_active * pred_num_products
        pred_bal_sal_ratio = pred_balance / pred_estimated_salary if pred_estimated_salary > 0 else 0

        st.metric("CLV Score", f"€{pred_clv_score:,.0f}")
        st.metric("Engagement Score", pred_engagement)
        st.metric("Balance/Salary Ratio", f"{pred_bal_sal_ratio:.2f}")

    if st.button("Predict Churn Risk", type="primary"):
        input_data = pd.DataFrame([{
            'CreditScore': pred_credit_score,
            'Gender': 1 if pred_gender == 'Female' else 0,
            'Age': pred_age,
            'Tenure': pred_tenure,
            'Balance': pred_balance,
            'NumOfProducts': pred_num_products,
            'HasCrCard': pred_has_cr_card,
            'IsActiveMember': pred_is_active,
            'EstimatedSalary': pred_estimated_salary,
            'CLV_Score': pred_clv_score,
            'EngagementScore': pred_engagement,
            'Balance_Salary_Ratio': pred_bal_sal_ratio,
            'Geography_France': 1 if pred_geography == 'France' else 0,
            'Geography_Germany': 1 if pred_geography == 'Germany' else 0,
            'Geography_Spain': 1 if pred_geography == 'Spain' else 0
        }])

        prob = model.predict_proba(input_data)[0][1]

        if prob >= 0.70:
            tier = "CRITICAL RISK"
            color = "#e74c3c"
            # FIX 2: Retention recommendation per risk tier
            recommendation = "🚨 Immediate action required. Assign a dedicated relationship manager. Schedule a personal call within 48 hours. Offer a premium loyalty package or interest rate review."
        elif prob >= 0.50:
            tier = "HIGH RISK"
            color = "#e67e22"
            recommendation = "⚠️ Priority outreach needed. Send a personalised engagement offer within 1 week. Consider product bundling or exclusive benefits to increase stickiness."
        elif prob >= 0.30:
            tier = "MEDIUM RISK"
            color = "#f39c12"
            recommendation = "📋 Monitor closely. Enrol in an automated re-engagement email sequence. Offer a product upgrade or credit card benefit to increase engagement score."
        else:
            tier = "LOW RISK"
            color = "#2ecc71"
            recommendation = "✅ Customer is stable. Maintain regular communication. Consider cross-selling additional products to move from 1 to 2 products — the safest retention zone."

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05);
                    border: 2px solid {color};
                    border-radius: 16px; padding: 24px;
                    text-align: center; margin-top: 20px;">
            <div style="font-size: 14px; color: #8B949E;
                        text-transform: uppercase;
                        letter-spacing: 2px;">Churn Probability</div>
            <div style="font-size: 48px; font-weight: 700;
                        color: {color};">{prob*100:.1f}%</div>
            <div style="font-size: 18px; font-weight: 600;
                        color: {color};">{tier}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("###")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03);
                    border-left: 4px solid {color};
                    border-radius: 8px; padding: 16px; margin-top: 12px;">
            <div style="font-size: 11px; color: #8B949E;
                        text-transform: uppercase; letter-spacing: 1px;
                        margin-bottom: 8px;">Retention Recommendation</div>
            <div style="font-size: 14px; color: #FAFAFA;">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)


# ── TAB 6: RETENTION ROI SIMULATOR ──
with tab6:
    st.title("Retention ROI Simulator")
    st.caption("Calculate financial return of retention interventions")
    st.markdown("---")

    st.subheader("Simulation Parameters")

    s1, s2 = st.columns(2)

    with s1:
        total_churners = 2037
        avg_balance_churned = 185588094.63 / 2037

        churn_reduction = st.slider(
            "Expected Churn Reduction (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5
        )

        campaign_cost = st.number_input(
            "Campaign Cost per Customer (€)",
            min_value=0,
            max_value=5000,
            value=200,
            step=50
        )

        target_segment = st.selectbox(
            "Target Segment",
            options=['All Churners', 'Critical Risk Only',
                     'High + Critical Risk']
        )

    with s2:
        if target_segment == 'Critical Risk Only':
            target_customers = 232
            segment_churn_rate = 0.737
        elif target_segment == 'High + Critical Risk':
            target_customers = 232 + 213
            segment_churn_rate = 0.578
        else:
            target_customers = total_churners
            segment_churn_rate = 0.2037

        customers_saved = int(target_customers * churn_reduction / 100)
        revenue_saved = customers_saved * avg_balance_churned
        total_campaign_cost = target_customers * campaign_cost
        net_roi = revenue_saved - total_campaign_cost
        roi_percentage = (net_roi / total_campaign_cost * 100) \
                         if total_campaign_cost > 0 else 0

        st.markdown("### Simulation Results")
        st.markdown("---")

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Customers Targeted", f"{target_customers:,}")
            st.metric("Customers Saved", f"{customers_saved:,}")
        with m2:
            st.metric("Revenue Saved", f"€{revenue_saved/1e6:.2f}M")
            st.metric("Campaign Cost", f"€{total_campaign_cost:,}")

        if net_roi > 0:
            st.success(f"✅ Net ROI: €{net_roi/1e6:.2f}M ({roi_percentage:.0f}% return)")
        else:
            st.error(f"❌ Net Loss: €{abs(net_roi)/1e6:.2f}M — increase reduction % or lower cost")

    st.markdown("---")

    scenarios = list(range(5, 55, 5))
    roi_values = []

    for pct in scenarios:
        saved = int(target_customers * pct / 100)
        rev = saved * avg_balance_churned
        cost = target_customers * campaign_cost
        roi_values.append((rev - cost) / 1e6)

    fig_roi = px.line(
        x=scenarios,
        y=roi_values,
        title='Net ROI vs Churn Reduction % — Scenario Analysis',
        template='plotly_dark',
        markers=True
    )
    fig_roi.update_traces(
        line_color='#2B8EFF',
        marker_color='#2B8EFF'
    )
    fig_roi.add_hline(y=0, line_dash="dash",
                      line_color="#e74c3c",
                      annotation_text="Break Even")
    fig_roi.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Churn Reduction %',
        yaxis_title='Net ROI (€M)'
    )
    st.plotly_chart(fig_roi, use_container_width=True)
    st.caption("Drag the sliders above to see how ROI changes with different intervention strategies")
