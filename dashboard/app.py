import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from textwrap import dedent
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="OLA Electric — VoC Crisis Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# OLA BRAND THEME
# =============================================================================
OLA_YELLOW  = "#D6DF22"
OLA_BLACK   = "#0A0A0A"
BG_PRIMARY  = "#0F0F0F"
BG_CARD     = "#1A1A1A"
BG_SIDEBAR  = "#141414"
TEXT_WHITE  = "#FFFFFF"
TEXT_MUTED  = "#888888"
RED         = "#FF4444"
AMBER       = "#F4A261"
GREEN       = "#52B788"

CAT_COLORS = {
    'Software / App'          : OLA_YELLOW,
    'Service Center'          : RED,
    'Customer Care'           : '#FF6B6B',
    'Battery & Range'         : AMBER,
    'Delivery & Registration' : '#A8DADC',
    'Safety & Breakdown'      : '#C77DFF',
    'Spare Parts'             : '#E76F51',
    'Warranty & Refunds'      : '#80B918',
    'Pricing & Value'         : '#6A4C93',
    'Positive Experience'     : GREEN
}

LABEL_MAP = {
    'cat_service_center'       : 'Service Center',
    'cat_software_app'         : 'Software / App',
    'cat_battery_range'        : 'Battery & Range',
    'cat_customer_care'        : 'Customer Care',
    'cat_spare_parts'          : 'Spare Parts',
    'cat_warranty_refunds'     : 'Warranty & Refunds',
    'cat_delivery_registration': 'Delivery & Registration',
    'cat_safety_breakdown'     : 'Safety & Breakdown',
    'cat_pricing_value'        : 'Pricing & Value',
    'cat_positive_experience'  : 'Positive Experience'
}

CAT_COLS       = list(LABEL_MAP.keys())
COMPLAINT_COLS = [c for c in CAT_COLS if c != 'cat_positive_experience']

# =============================================================================
# GLOBAL CSS
# =============================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset & Base */
*, *::before, *::after {{ box-sizing: border-box; }}

.stApp {{
    background-color: {BG_PRIMARY};
    font-family: 'DM Sans', sans-serif;
    color: {TEXT_WHITE};
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {BG_SIDEBAR} !important;
    border-right: 1px solid #2A2A2A;
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_WHITE} !important;
}}

/* Hide default streamlit elements */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem; padding-bottom: 2rem; }}

/* Metric cards */
[data-testid="metric-container"] {{
    background: {BG_CARD};
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 1rem;
}}

[data-testid="stMetricValue"] {{
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: {OLA_YELLOW} !important;
}}

[data-testid="stMetricLabel"] {{
    font-family: 'DM Sans', sans-serif !important;
    color: {TEXT_MUTED} !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

[data-testid="stMetricDelta"] {{
    font-size: 0.75rem !important;
}}

/* Selectbox and sliders */
.stSelectbox > div > div {{
    background: {BG_CARD} !important;
    border: 1px solid #333 !important;
    color: {TEXT_WHITE} !important;
}}

/* Plotly charts background */
.js-plotly-plot .plotly .main-svg {{
    background: transparent !important;
}}

/* Custom card */
.ola-card {{
    background: {BG_CARD};
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}}

.ola-card-accent {{
    border-left: 3px solid {OLA_YELLOW};
}}

.ola-card-danger {{
    border-left: 3px solid {RED};
}}

/* Page title */
.page-title {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: {OLA_YELLOW};
    letter-spacing: 0.02em;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}}

.page-subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: {TEXT_MUTED};
    margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}}

/* Section header */
.section-header {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: {TEXT_WHITE};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-bottom: 1px solid #2A2A2A;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
}}

/* Insight pill */
.insight-pill {{
    display: inline-block;
    background: rgba(214,223,34,0.12);
    border: 1px solid rgba(214,223,34,0.3);
    border-radius: 4px;
    padding: 0.15rem 0.6rem;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    color: {OLA_YELLOW};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-right: 0.4rem;
}}

.insight-pill-red {{
    background: rgba(255,68,68,0.12);
    border-color: rgba(255,68,68,0.3);
    color: {RED};
}}

/* Review card */
.review-card {{
    background: #111;
    border: 1px solid #252525;
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    line-height: 1.6;
}}

.review-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: {TEXT_MUTED};
    margin-bottom: 0.4rem;
}}

/* Sidebar logo */
.sidebar-logo {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: {OLA_YELLOW};
    letter-spacing: 0.1em;
    padding: 1rem 0 0.5rem 0;
}}

.sidebar-tagline {{
    font-size: 0.7rem;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}}

/* Recommendation card */
.rec-card {{
    background: {BG_CARD};
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}}

.rec-priority-critical {{
    border-left: 4px solid {RED};
}}

.rec-priority-high {{
    border-left: 4px solid {AMBER};
}}

.rec-priority-medium {{
    border-left: 4px solid {OLA_YELLOW};
}}

/* Table styling */
.dataframe {{
    background: {BG_CARD} !important;
    color: {TEXT_WHITE} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: {BG_CARD};
    border-radius: 8px;
    gap: 0;
}}

.stTabs [data-baseweb="tab"] {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: {TEXT_MUTED};
    padding: 0.6rem 1.2rem;
}}

.stTabs [aria-selected="true"] {{
    color: {OLA_YELLOW} !important;
    border-bottom: 2px solid {OLA_YELLOW} !important;
    background: transparent !important;
}}

/* Divider */
.ola-divider {{
    border: none;
    border-top: 1px solid #1E1E1E;
    margin: 1.5rem 0;
}}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv('data/classified/ola_reviews_classified.csv')
    df['at'] = pd.to_datetime(df['at'])
    df['year_month'] = pd.to_datetime(df['year_month'])
    for col in CAT_COLS:
        if col in df.columns:
            df[col] = df[col].astype(bool)
    return df

@st.cache_data
def load_monthly():
    monthly = pd.read_csv('data/cleaned/ola_monthly_trends.csv')
    monthly['year_month'] = pd.to_datetime(monthly['year_month'])
    return monthly

df      = load_data()
monthly = load_monthly()

# =============================================================================
# PLOTLY THEME
# =============================================================================
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=40, b=10)
)

FONT_DEFAULT = dict(
    family='DM Sans',
    color=TEXT_WHITE,
    size=11
)

XAXIS_DEFAULT = dict(
    gridcolor='#1E1E1E',
    linecolor='#2A2A2A',
    tickcolor='#2A2A2A'
)

YAXIS_DEFAULT = dict(
    gridcolor='#1E1E1E',
    linecolor='#2A2A2A',
    tickcolor='#2A2A2A'
)

LEGEND_DEFAULT = dict(
    bgcolor='rgba(0,0,0,0)',
    bordercolor='#2A2A2A'
)
# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">⚡ OLA ELECTRIC</div>
    <div class="sidebar-tagline">Voice of Customer — Crisis Analysis</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**NAVIGATION**")

    page = st.radio(
        label="",
        options=[
            "📊 Executive Overview",
            "🔍 Complaint Intelligence",
            "📈 Crisis Timeline",
            "🔬 Complaint Explorer",
            "💡 Recommendations",
            "📋 Case Study"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**GLOBAL FILTERS**")

    # Date range
    min_date = df['at'].min().date()
    max_date = df['at'].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Star rating filter
    rating_filter = st.multiselect(
        "Star Rating",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5],
        format_func=lambda x: f"{'⭐' * x} ({x} star)"
    )

    # Review type
    review_type = st.selectbox(
        "Review Type",
        options=["All Reviews", "Complaints Only", "Positive Only"]
    )

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.7rem; color:{TEXT_MUTED}; line-height:1.6;'>
    <b style='color:{OLA_YELLOW}'>Dataset</b><br>
    {len(df):,} reviews<br>
    May 2022 — Jun 2026<br><br>
    <b style='color:{OLA_YELLOW}'>Methodology</b><br>
    VADER Sentiment<br>
    Multi-label Classifier<br>
    99.2% validation accuracy<br><br>
    <b style='color:{OLA_YELLOW}'>Built by</b><br>
    Naren Karthikeyan A
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# APPLY FILTERS
# =============================================================================
if len(date_range) == 2:
    start_date, end_date = date_range
    dff = df[
        (df['at'].dt.date >= start_date) &
        (df['at'].dt.date <= end_date)
    ]
else:
    dff = df.copy()

if rating_filter:
    dff = dff[dff['score'].isin(rating_filter)]

if review_type == "Complaints Only":
    dff = dff[dff['complaint_count'] > 0]
elif review_type == "Positive Only":
    dff = dff[dff['cat_positive_experience'] == True]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def kpi_card(col, label, value, delta=None, delta_color="normal"):
    col.metric(label=label, value=value, delta=delta, delta_color=delta_color)

def plotly_bar_h(data, x, y, title, color_map=None):
    colors = [color_map.get(c, OLA_YELLOW) for c in data[y]] if color_map else OLA_YELLOW
    fig = go.Figure(go.Bar(
        x=data[x], y=data[y],
        orientation='h',
        marker_color=colors,
        marker_line_width=0
    ))
    fig.update_layout(
    **PLOT_LAYOUT,
    font=FONT_DEFAULT,
    legend={
        **LEGEND_DEFAULT,
        "orientation": "h",
        "y": 1.1
    }
)
    fig.update_yaxes(gridcolor='#1E1E1E', linecolor='#2A2A2A', tickcolor='#2A2A2A')
    return fig

def get_cat_metrics():
    rows = []
    for col in COMPLAINT_COLS:
        subset = dff[dff[col] == True]
        if len(subset) == 0:
            continue
        rows.append({
            'Category'     : LABEL_MAP[col],
            'Count'        : len(subset),
            'Pct'          : len(subset) / len(dff) * 100,
            'Avg_Sentiment': subset['sentiment_score'].mean(),
            'Avg_Rating'   : subset['score'].mean(),
            'Pct_1star'    : (subset['score'] == 1).mean() * 100
        })
    return pd.DataFrame(rows).sort_values('Count', ascending=False)

# =============================================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# =============================================================================
if page == "📊 Executive Overview":

    st.markdown('<div class="page-title">EXECUTIVE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">OLA Electric · Customer Experience Crisis · 2022–2026</div>', unsafe_allow_html=True)

    # KPI Row
    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_card(k1, "Reviews Analyzed", f"{len(dff):,}")
    kpi_card(k2, "Avg Star Rating", f"{dff['score'].mean():.2f} / 5.0",
             delta=f"{dff['score'].mean()-4.0:.2f} vs benchmark")
    kpi_card(k3, "1-Star Reviews", f"{(dff['score']==1).mean()*100:.1f}%",
             delta="Industry avg ~15%", delta_color="inverse")
    kpi_card(k4, "Negative Sentiment", f"{(dff['sentiment_label']=='Negative').mean()*100:.1f}%")
    kpi_card(k5, "Developer Reply Rate", "0.0%",
             delta="Industry avg 40-60%", delta_color="inverse")

    st.markdown("<hr class='ola-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        # Rating distribution
        rating_dist = dff['score'].value_counts().sort_index().reset_index()
        rating_dist.columns = ['Rating', 'Count']
        rating_dist['Label'] = rating_dist['Rating'].apply(lambda x: f"{'⭐'*x}")
        rating_dist['Color'] = rating_dist['Rating'].map({
            1: RED, 2: '#FF6B6B', 3: AMBER, 4: '#A8C686', 5: GREEN
        })

        fig = go.Figure(go.Bar(
            x=rating_dist['Label'],
            y=rating_dist['Count'],
            marker_color=rating_dist['Color'],
            marker_line_width=0,
            text=rating_dist['Count'].apply(lambda x: f"{x:,}"),
            textposition='outside',
            textfont=dict(color=TEXT_WHITE, size=10)
        ))
        fig.update_layout(
            title="Star Rating Distribution",
            **PLOT_LAYOUT,
            yaxis_title="Number of Reviews"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Sentiment donut
        sent_counts = dff['sentiment_label'].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=sent_counts.index,
            values=sent_counts.values,
            hole=0.65,
            marker_colors=[RED, GREEN, AMBER],
            textfont=dict(size=11),
            hovertemplate="%{label}: %{value:,} reviews<br>%{percent}<extra></extra>"
        ))
        fig2.add_annotation(
            text=f"<b style='font-size:20px'>{dff['sentiment_score'].mean():.2f}</b><br>avg score",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color=TEXT_WHITE, size=12)
        )
        fig2.update_layout(
            title="Sentiment Distribution",
            **PLOT_LAYOUT,
            showlegend=True,
            legend=dict(orientation='h', y=-0.1)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Executive insights
    st.markdown('<div class="section-header">Executive Insights</div>', unsafe_allow_html=True)

    insights = [
        ("OBSERVATION", f"Software/App complaints dominate at {dff['cat_software_app'].mean()*100:.1f}% of all reviews — nearly 5× the next highest category.", "accent"),
        ("CRITICAL", f"Customer Care complaints produce a {(dff[dff['cat_customer_care']==True]['score']==1).mean()*100:.1f}% one-star rate — the highest of any category.", "danger"),
        ("OBSERVATION", "OLA Electric has maintained a 0% developer response rate across 4 years and 7,119 reviews. Industry benchmark: 40–60%.", "danger"),
        ("FINDING", "Review volume spiked 274% between June and July 2025 — correlating with the second CCPA show-cause notice period.", "accent"),
        ("CONCLUSION", "Sentiment differs significantly across complaint categories (Kruskal-Wallis H=274.3, p<0.001). Not all failures feel equally damaging.", "accent"),
    ]

    for label, text, style in insights:
        pill_class = "insight-pill" if style == "accent" else "insight-pill insight-pill-red"
        st.markdown(f"""
        <div class="ola-card {'ola-card-accent' if style == 'accent' else 'ola-card-danger'}">
            <span class="{pill_class}">{label}</span>
            <span style='font-size:0.88rem; color:{TEXT_WHITE};'>{text}</span>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE 2 — COMPLAINT INTELLIGENCE
# =============================================================================
elif page == "🔍 Complaint Intelligence":

    st.markdown('<div class="page-title">COMPLAINT INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">What is breaking — and how severely?</div>', unsafe_allow_html=True)

    cat_metrics = get_cat_metrics()

    col1, col2 = st.columns([3, 2])

    with col1:
        fig = plotly_bar_h(
            cat_metrics, 'Count', 'Category',
            'Complaint Frequency by Category',
            color_map=CAT_COLORS
        )
        fig.update_traces(
            text=cat_metrics['Count'].apply(lambda x: f"{x:,}  ({x/len(dff)*100:.1f}%)"),
            textposition='outside',
            textfont=dict(size=9, color=TEXT_WHITE)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Avg rating by category
        fig2 = plotly_bar_h(
            cat_metrics.sort_values('Avg_Rating'),
            'Avg_Rating', 'Category',
            'Avg Star Rating by Category',
            color_map=CAT_COLORS
        )
        fig2.update_traces(
            text=cat_metrics.sort_values('Avg_Rating')['Avg_Rating'].apply(lambda x: f"{x:.2f}★"),
            textposition='outside',
            textfont=dict(size=9, color=TEXT_WHITE)
        )
        fig2.update_xaxes(range=[0, 5])
        st.plotly_chart(fig2, use_container_width=True)

    # Rich metrics table
    st.markdown('<div class="section-header">Rich Metrics Table</div>', unsafe_allow_html=True)

    display_df = cat_metrics.copy()
    display_df['Count']         = display_df['Count'].apply(lambda x: f"{x:,}")
    display_df['Pct']           = display_df['Pct'].apply(lambda x: f"{x:.1f}%")
    display_df['Avg_Sentiment'] = display_df['Avg_Sentiment'].apply(lambda x: f"{x:.3f}")
    display_df['Avg_Rating']    = display_df['Avg_Rating'].apply(lambda x: f"{x:.2f}")
    display_df['Pct_1star']     = display_df['Pct_1star'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['Category','Count','% Reviews','Avg Sentiment','Avg Rating','1-Star Rate']

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<hr class='ola-divider'>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        # Rating heatmap by category
        heatmap_data = []
        for col in COMPLAINT_COLS:
            subset = dff[dff[col] == True]
            if len(subset) == 0:
                continue
            row = {'Category': LABEL_MAP[col]}
            for star in [1, 2, 3, 4, 5]:
                row[f'{star}★'] = (subset['score'] == star).mean() * 100
            heatmap_data.append(row)

        hmap_df = pd.DataFrame(heatmap_data).set_index('Category')

        fig3 = go.Figure(go.Heatmap(
            z=hmap_df.values,
            x=hmap_df.columns.tolist(),
            y=hmap_df.index.tolist(),
            colorscale=[[0,'#1A1A1A'],[0.3,AMBER],[1.0,RED]],
            text=[[f"{v:.1f}%" for v in row] for row in hmap_df.values],
            texttemplate="%{text}",
            textfont=dict(size=10),
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT_WHITE))
        ))
        fig3.update_layout(
            title="% Star Rating by Complaint Category",
            **PLOT_LAYOUT,
            yaxis=dict(autorange='reversed', gridcolor='#1E1E1E')
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Complaint complexity
        count_dist = dff['complaint_count'].value_counts().sort_index()
        fig4 = go.Figure(go.Bar(
            x=count_dist.index,
            y=count_dist.values,
            marker_color=[GREEN if i == 0 else AMBER if i <= 2 else RED
                          for i in count_dist.index],
            marker_line_width=0,
            text=[f"{v:,}\n({v/len(dff)*100:.1f}%)" for v in count_dist.values],
            textposition='outside',
            textfont=dict(size=9, color=TEXT_WHITE)
        ))
        fig4.update_layout(
            title="Complaint Complexity Distribution",
            xaxis_title="Number of Complaint Categories per Review",
            yaxis_title="Reviews",
            **PLOT_LAYOUT
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Top complaint pairs
    st.markdown('<div class="section-header">Top Co-occurring Complaint Pairs</div>', unsafe_allow_html=True)
    from itertools import combinations

    pair_counts = {}
    for _, row in dff[COMPLAINT_COLS].iterrows():
        active = [LABEL_MAP[col] for col in COMPLAINT_COLS if row[col]]
        for pair in combinations(active, 2):
            key = f"{pair[0]}  +  {pair[1]}"
            pair_counts[key] = pair_counts.get(key, 0) + 1

    pairs_df = pd.DataFrame(
        sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        columns=['Complaint Pair', 'Co-occurrences']
    )

    fig5 = go.Figure(go.Bar(
        x=pairs_df['Co-occurrences'],
        y=pairs_df['Complaint Pair'],
        orientation='h',
        marker_color=OLA_YELLOW,
        marker_line_width=0,
        text=pairs_df['Co-occurrences'],
        textposition='outside',
        textfont=dict(size=9, color=TEXT_WHITE)
    ))
    fig5.update_layout(
        title="Top 10 Co-occurring Complaint Pairs",
        **PLOT_LAYOUT,
        yaxis=dict(autorange='reversed', gridcolor='#1E1E1E')
    )
    st.plotly_chart(fig5, use_container_width=True)

# =============================================================================
# PAGE 3 — CRISIS TIMELINE
# =============================================================================
elif page == "📈 Crisis Timeline":

    st.markdown('<div class="page-title">CRISIS TIMELINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">When did it start — and is it recovering?</div>', unsafe_allow_html=True)

    # Verified OLA events
    EVENTS = [
        {'date': '2021-12-01', 'label': 'S1 Pro Delivered',       'y': 0.95},
        {'date': '2023-08-15', 'label': 'New Models Announced',   'y': 0.85},
        {'date': '2024-08-09', 'label': 'IPO Listed ₹76/share',   'y': 0.95},
        {'date': '2024-10-07', 'label': 'CCPA Notice #1',         'y': 0.75},
        {'date': '2024-12-04', 'label': 'CCPA Notice #2',         'y': 0.85},
    ]

    monthly_filt = monthly[monthly['review_count'] >= 10].copy()

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=("Monthly Review Volume", "Average Star Rating", "Average Sentiment Score"),
        vertical_spacing=0.08,
        row_heights=[0.35, 0.32, 0.33]
    )

    # Row 1 — Volume
    fig.add_trace(go.Scatter(
        x=monthly_filt['year_month'], y=monthly_filt['review_count'],
        fill='tozeroy', fillcolor=f'rgba(70,123,157,0.15)',
        line=dict(color='#457B9D', width=2),
        name='Review Volume',
        hovertemplate="%{x|%b %Y}: %{y:,} reviews<extra></extra>"
    ), row=1, col=1)

    # Row 2 — Avg Rating
    fig.add_trace(go.Scatter(
        x=monthly_filt['year_month'], y=monthly_filt['avg_rating'],
        line=dict(color=RED, width=2),
        mode='lines+markers', marker=dict(size=4),
        name='Avg Rating',
        hovertemplate="%{x|%b %Y}: %{y:.2f}★<extra></extra>"
    ), row=2, col=1)
    fig.add_hline(y=3.0, line_dash='dash', line_color='#444',
                  annotation_text="Neutral (3.0)", row=2, col=1)

    # Row 3 — Sentiment
    fig.add_trace(go.Scatter(
        x=monthly_filt['year_month'], y=monthly_filt['avg_sentiment_score'],
        line=dict(color=OLA_YELLOW, width=2),
        mode='lines+markers', marker=dict(size=4),
        name='Avg Sentiment',
        hovertemplate="%{x|%b %Y}: %{y:.3f}<extra></extra>"
    ), row=3, col=1)
    fig.add_hline(y=0, line_dash='dash', line_color='#444', row=3, col=1)

    # Add event annotations to row 1
    for event in EVENTS:
        fig.add_vline(
            x=event['date'],
            line_dash='dot', line_color='rgba(214,223,34,0.4)',
            line_width=1
        )
        fig.add_annotation(
            x=event['date'],
            y=event['y'],
            yref='y',
            text=event['label'],
            showarrow=True,
            arrowhead=1,
            arrowcolor=OLA_YELLOW,
            font=dict(size=9, color=OLA_YELLOW),
            bgcolor='rgba(26,26,26,0.9)',
            bordercolor=OLA_YELLOW,
            borderwidth=1,
            row=1, col=1
        )

    fig.update_layout(
        height=650,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color=TEXT_WHITE, size=10),
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )
    fig.update_xaxes(gridcolor='#1E1E1E', linecolor='#2A2A2A')
    fig.update_yaxes(gridcolor='#1E1E1E', linecolor='#2A2A2A', tickcolor='#2A2A2A')

    st.plotly_chart(fig, use_container_width=True)

    # Pre vs Post comparison
    st.markdown('<div class="section-header">Pre vs Post Crisis Comparison</div>', unsafe_allow_html=True)

    pre  = dff[dff['at'] < '2025-07-01']
    post = dff[dff['at'] >= '2025-07-01']

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pre-Crisis Avg Rating",   f"{pre['score'].mean():.2f}★")
    c2.metric("Post-Crisis Avg Rating",  f"{post['score'].mean():.2f}★",
              delta=f"{post['score'].mean()-pre['score'].mean():.2f}")
    c3.metric("Pre-Crisis Sentiment",    f"{pre['sentiment_score'].mean():.3f}")
    c4.metric("Post-Crisis Sentiment",   f"{post['sentiment_score'].mean():.3f}",
              delta=f"{post['sentiment_score'].mean()-pre['sentiment_score'].mean():.3f}")

    st.markdown(f"""
    <div class="ola-card ola-card-accent" style='margin-top:1rem;'>
        <span class="insight-pill">CONCLUSION</span>
        <span style='font-size:0.88rem;'>
        Post-July 2025 sentiment is significantly higher than pre-crisis sentiment
        (Mann-Whitney U, p=3.74e-50). However this reflects <b>reviewer population change</b>
        — the most negative customers disengaged — not genuine service recovery.
        Average star ratings remain below 2.5 throughout 2026.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Monthly table
    st.markdown('<div class="section-header">Monthly Trends Data</div>', unsafe_allow_html=True)

    year_filter = st.selectbox(
        "Filter by year",
        options=["All"] + sorted(monthly['year_month'].dt.year.unique().tolist(), reverse=True)
    )

    monthly_display = monthly_filt.copy()
    if year_filter != "All":
        monthly_display = monthly_display[
            monthly_display['year_month'].dt.year == int(year_filter)
        ]

    monthly_display['year_month'] = monthly_display['year_month'].dt.strftime('%Y-%m')
    monthly_display = monthly_display.rename(columns={
        'year_month'         : 'Month',
        'review_count'       : 'Reviews',
        'avg_rating'         : 'Avg Rating',
        'pct_one_star'       : '% 1-Star',
        'pct_negative'       : '% Negative',
        'avg_sentiment_score': 'Avg Sentiment',
        'avg_review_length'  : 'Avg Length'
    })

    cols_show = ['Month','Reviews','Avg Rating','% 1-Star','% Negative','Avg Sentiment']
    st.dataframe(
        monthly_display[cols_show].round(2),
        use_container_width=True,
        hide_index=True
    )

# =============================================================================
# PAGE 4 — COMPLAINT EXPLORER
# =============================================================================
elif page == "🔬 Complaint Explorer":

    st.markdown('<div class="page-title">COMPLAINT EXPLORER</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Deep dive into any complaint category</div>', unsafe_allow_html=True)

    # Category selector
    selected_label = st.selectbox(
        "Select Complaint Category",
        options=[LABEL_MAP[c] for c in COMPLAINT_COLS]
    )

    selected_col = [k for k, v in LABEL_MAP.items() if v == selected_label][0]
    subset = dff[dff[selected_col] == True]

    if len(subset) == 0:
        st.warning("No reviews found for this category with current filters.")
    else:
        # KPI row
        k1, k2, k3, k4, k5 = st.columns(5)
        kpi_card(k1, "Reviews",          f"{len(subset):,}")
        kpi_card(k2, "% of All Reviews", f"{len(subset)/len(dff)*100:.1f}%")
        kpi_card(k3, "Avg Star Rating",  f"{subset['score'].mean():.2f}★")
        kpi_card(k4, "Avg Sentiment",    f"{subset['sentiment_score'].mean():.3f}")
        kpi_card(k5, "1-Star Rate",      f"{(subset['score']==1).mean()*100:.1f}%")

        st.markdown("<hr class='ola-divider'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])

        with col1:
            # Monthly trend for this category
            monthly_cat = dff.copy()
            monthly_cat['year_month_dt'] = pd.to_datetime(monthly_cat['year_month'])
            cat_trend = monthly_cat[monthly_cat[selected_col] == True].groupby(
                monthly_cat['year_month_dt'].dt.to_period('M').dt.to_timestamp()
            ).agg(
                count=('reviewId', 'count'),
                avg_sentiment=('sentiment_score', 'mean')
            ).reset_index()
            cat_trend.columns = ['month', 'count', 'avg_sentiment']

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=cat_trend['month'], y=cat_trend['count'],
                name='Volume',
                marker_color=CAT_COLORS.get(selected_label, OLA_YELLOW),
                opacity=0.7
            ))
            fig.add_trace(go.Scatter(
                x=cat_trend['month'], y=cat_trend['avg_sentiment'],
                name='Avg Sentiment',
                yaxis='y2',
                line=dict(color=TEXT_WHITE, width=2),
                mode='lines+markers', marker=dict(size=5)
            ))
            fig.update_layout(
                title=f"{selected_label} — Monthly Volume & Sentiment",
                yaxis=dict(title='Reviews', gridcolor='#1E1E1E'),
                yaxis2=dict(title='Sentiment', overlaying='y', side='right',
                           gridcolor='#1E1E1E', zeroline=True,
                           zerolinecolor='#444'),
                **PLOT_LAYOUT,
                legend=dict(orientation='h', y=1.1)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Co-occurrence
            cooc = []
            for other_col in COMPLAINT_COLS:
                if other_col == selected_col:
                    continue
                overlap = dff[(dff[selected_col] == True) & (dff[other_col] == True)]
                if len(overlap) > 0:
                    cooc.append({
                        'Category': LABEL_MAP[other_col],
                        'Count': len(overlap),
                        'Rate': len(overlap) / len(subset) * 100
                    })

            if cooc:
                cooc_df = pd.DataFrame(cooc).sort_values('Count', ascending=False)
                fig2 = go.Figure(go.Bar(
                    x=cooc_df['Count'],
                    y=cooc_df['Category'],
                    orientation='h',
                    marker_color=[CAT_COLORS.get(c, OLA_YELLOW) for c in cooc_df['Category']],
                    marker_line_width=0,
                    text=[f"{r:.1f}%" for r in cooc_df['Rate']],
                    textposition='outside',
                    textfont=dict(size=9, color=TEXT_WHITE)
                ))
                fig2.update_layout(
                    title="Co-occurring Categories",
                    **PLOT_LAYOUT,
                    yaxis=dict(autorange='reversed', gridcolor='#1E1E1E')
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Sample Reviews
        st.markdown('<div class="section-header">Sample Reviews</div>', unsafe_allow_html=True)

        n_samples = st.slider("Number of reviews", 3, 20, 8)
        sort_by   = st.selectbox("Sort by", ["Most Thumbs Up", "Most Negative", "Most Recent"])

        if sort_by == "Most Thumbs Up":
            samples = subset.nlargest(n_samples, 'thumbsUpCount')
        elif sort_by == "Most Negative":
            samples = subset.nsmallest(n_samples, 'sentiment_score')
        else:
            samples = subset.nlargest(n_samples, 'at')

        for _, row in samples.iterrows():
            stars = "⭐" * int(row['score'])
            sentiment_color = RED if row['sentiment_score'] < -0.05 else (
                GREEN if row['sentiment_score'] > 0.05 else AMBER
            )
            st.markdown(f"""
            <div class="review-card">
                <div class="review-meta">
                    {stars} &nbsp;|&nbsp;
                    <span style='color:{sentiment_color}'>
                        sentiment {row['sentiment_score']:.2f}
                    </span> &nbsp;|&nbsp;
                    {row['at']:%d %b %Y} &nbsp;|&nbsp;
                    👍 {int(row['thumbsUpCount'])}
                </div>
                {row['content']}
            </div>
            """, unsafe_allow_html=True)

        # Review Journey
        st.markdown(
    '<div class="section-header">⭐ Review Journey</div>',
    unsafe_allow_html=True
    )

        st.markdown(
    f"""
<div style="font-size:0.8rem;color:{TEXT_MUTED};margin-bottom:1rem;">
Select a review to trace the analytical pipeline from raw text to business action.
</div>
""",
    unsafe_allow_html=True
)

        journey_samples = subset.nlargest(10, "thumbsUpCount")

        journey_idx = st.selectbox(
    "Select review",
    options=range(len(journey_samples)),
    format_func=lambda i: journey_samples.iloc[i]["content"][:80] + "..."
)

        if journey_idx is not None:

            jrow = journey_samples.iloc[journey_idx]

            active_cats = [
        LABEL_MAP[c]
        for c in COMPLAINT_COLS
        if jrow.get(c, False)
    ]

    sentiment_score = jrow["sentiment_score"]
    sentiment_label = jrow["sentiment_label"]
    star = int(jrow["score"])

    sentiment_color = (
        RED if sentiment_score < -0.05
        else GREEN if sentiment_score > 0.05
        else AMBER
    )

    rec_map = {
        "Service Center":
            "Reduce repair turnaround time. Implement proactive SMS updates.",

        "Software / App":
            "Deploy OTA fix for connectivity and login issues. Priority: Bluetooth F002 error.",

        "Customer Care":
            "Enforce 24-hour response SLA. Begin responding to Play Store reviews.",

        "Battery & Range":
            "Investigate BMS firmware and improve battery estimation accuracy.",

        "Spare Parts":
            "Maintain minimum regional inventory and expose parts availability.",

        "Warranty & Refunds":
            "Audit warranty rejection decisions and simplify policy.",

        "Delivery & Registration":
            "Provide real-time delivery tracking and accelerate RC processing.",

        "Safety & Breakdown":
            "Escalate all safety incidents through a dedicated response team.",

        "Pricing & Value":
            "Review OLA Care Plus pricing and improve charge transparency."
    }

    category_html = ""

    if active_cats:

        for cat in active_cats:

            category_html += f"""
<div style="
color:{CAT_COLORS.get(cat, OLA_YELLOW)};
font-size:0.82rem;
margin:0.25rem 0;
">
✓ {cat}
</div>
"""

    else:

        category_html = """
<div style="color:#777;font-size:0.82rem;">
Uncategorized
</div>
"""

    recommendation_html = ""

    if active_cats:

        for cat in active_cats:

            recommendation_html += f"""
<div style="
font-size:0.82rem;
margin:0.35rem 0;
color:white;
">
→ {rec_map.get(cat, "Escalate for further investigation.")}
</div>
"""

    else:

        recommendation_html = """
<div style="font-size:0.82rem;color:#777;">
No operational recommendation available.
</div>
"""

    html = dedent(f"""
<div style="display:flex;
gap:12px;
align-items:stretch;
flex-wrap:wrap;
margin-top:1rem;
margin-bottom:1rem;">

<div class="ola-card"
style="flex:2;padding:1rem;">

<div style="font-size:0.65rem;
color:{TEXT_MUTED};
text-transform:uppercase;
letter-spacing:0.08em;
margin-bottom:0.5rem;">
Raw Review
</div>

<div style="font-size:0.9rem;
line-height:1.6;">
{jrow["content"][:300]}
{"..." if len(str(jrow["content"]))>300 else ""}
</div>

</div>

<div style="
display:flex;
align-items:center;
font-size:1.4rem;
color:#555;">
➜
</div>

<div class="ola-card"
style="flex:1;padding:1rem;">

<div style="font-size:0.65rem;
color:{TEXT_MUTED};
text-transform:uppercase;
letter-spacing:0.08em;
margin-bottom:0.5rem;">
Complaint Categories
</div>

{category_html}

</div>

<div style="
display:flex;
align-items:center;
font-size:1.4rem;
color:#555;">
➜
</div>

<div class="ola-card"
style="flex:1;padding:1rem;">

<div style="font-size:0.65rem;
color:{TEXT_MUTED};
text-transform:uppercase;
letter-spacing:0.08em;
margin-bottom:0.5rem;">
Sentiment
</div>

<div style="
font-family:Rajdhani;
font-size:1.6rem;
font-weight:700;
color:{sentiment_color};">
{sentiment_score:+.2f}
</div>

<div style="
font-size:0.8rem;
color:{TEXT_MUTED};">
{sentiment_label} · {"⭐"*star}
</div>

</div>

<div style="
display:flex;
align-items:center;
font-size:1.4rem;
color:#555;">
➜
</div>

<div class="ola-card ola-card-accent"
style="flex:2;padding:1rem;">

<div style="
font-size:0.65rem;
color:{OLA_YELLOW};
text-transform:uppercase;
letter-spacing:0.08em;
margin-bottom:0.5rem;">
Recommended Action
</div>

{recommendation_html}

</div>

</div>
""")

    st.markdown(html, unsafe_allow_html=True)

# =============================================================================
# PAGE 5 — RECOMMENDATIONS
# =============================================================================
elif page == "💡 Recommendations":

    st.markdown('<div class="page-title">RECOMMENDATIONS</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Data-backed interventions prioritized by severity × volume</div>', unsafe_allow_html=True)

    # Priority matrix bubble chart
    cat_metrics = get_cat_metrics()
    fig = go.Figure()

    for _, row in cat_metrics.iterrows():
        severity = 6 - row['Avg_Rating']
        volume   = row['Count']
        fig.add_trace(go.Scatter(
            x=[row['Pct']],
            y=[row['Pct_1star']],
            mode='markers+text',
            marker=dict(
                size=np.sqrt(volume) * 2,
                color=CAT_COLORS.get(row['Category'], OLA_YELLOW),
                opacity=0.85,
                line=dict(color='white', width=1)
            ),
            text=[row['Category']],
            textposition='top center',
            textfont=dict(size=9, color=TEXT_WHITE),
            name=row['Category'],
            hovertemplate=(
                f"<b>{row['Category']}</b><br>"
                f"Volume: {row['Count']:,} reviews ({row['Pct']:.1f}%)<br>"
                f"1-Star Rate: {row['Pct_1star']:.1f}%<br>"
                f"Avg Rating: {row['Avg_Rating']:.2f}★<extra></extra>"
            )
        ))

    fig.update_layout(
        title="Priority Matrix — Volume (x) vs Severity (y) vs Count (size)",
        xaxis_title="% of All Reviews (Volume)",
        yaxis_title="1-Star Rate % (Severity)",
        showlegend=False,
        **PLOT_LAYOUT
    )
    fig.add_annotation(
        x=45, y=95,
        text="HIGH PRIORITY →",
        showarrow=False,
        font=dict(color=RED, size=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recommendation cards
    st.markdown('<div class="section-header">Prioritized Recommendations</div>', unsafe_allow_html=True)

    recs = [
        {
            'priority'  : 'CRITICAL',
            'title'     : 'Rebuild Customer Care as Priority Infrastructure',
            'category'  : 'Customer Care',
            'owner'     : 'Customer Experience',
            'evidence'  : '93.9% one-star rate — highest of any category. Mann-Whitney U p<0.001.',
            'actions'   : [
                'Enforce 24h response SLA with escalation at 48h',
                'Implement visible ticket tracking inside app',
                'Begin responding to Play Store reviews immediately',
                'Report monthly resolution rate publicly'
            ],
            'impact'    : 'HIGH — directly addresses category with most damaged relationships'
        },
        {
            'priority'  : 'CRITICAL',
            'title'     : 'Fix the App — Highest Volume, Fastest ROI',
            'category'  : 'Software / App',
            'owner'     : 'Product & Engineering',
            'evidence'  : '50.5% of all reviews. App failure co-occurs with 6 of top 10 complaint pairs.',
            'actions'   : [
                'Fix Bluetooth F002 connectivity error (repeatedly cited)',
                'Resolve login/authentication blank screen failures',
                'Restore accurate battery % and location display',
                'Implement push notifications for charging status'
            ],
            'impact'    : 'HIGH — reducing app complaints 50% removes issue from ~25% of all reviews'
        },
        {
            'priority'  : 'HIGH',
            'title'     : 'Treat Service Center + Spare Parts as One System',
            'category'  : 'Service Center + Spare Parts',
            'owner'     : 'Operations + Procurement',
            'evidence'  : 'Co-occur in 336 reviews. Spare Parts has most negative sentiment (-0.385).',
            'actions'   : [
                'Mandate minimum spare parts inventory at each service center',
                'Publish estimated repair timelines at job card creation',
                'Proactive SMS notification when parts arrive',
                'Target: maximum 15-day repair turnaround for common components'
            ],
            'impact'    : 'HIGH — addresses second-lowest avg rating (1.28) and highest severity sentiment'
        },
        {
            'priority'  : 'MEDIUM',
            'title'     : 'Activate Play Store as Customer Recovery Channel',
            'category'  : 'Developer Engagement',
            'owner'     : 'Customer Experience / Marketing',
            'evidence'  : '0% response rate across 7,119 reviews and 4 years.',
            'actions'   : [
                'Assign dedicated resource for Play Store responses',
                'Priority queue: 1-star reviews with 10+ thumbs-up',
                'Response template: acknowledge + ticket number + timeline',
                'Target: 40% response rate on 1-star reviews within 30 days'
            ],
            'impact'    : 'MEDIUM — visible accountability signals to prospective buyers'
        },
        {
            'priority'  : 'MEDIUM',
            'title'     : 'Implement Review-Based Early Warning System',
            'category'  : 'Data Infrastructure',
            'owner'     : 'Data / Product',
            'evidence'  : 'Word count correlates with severity (Spearman r=-0.369, p<0.001).',
            'actions'   : [
                'Automate Play Store review monitoring pipeline',
                'Flag: word count >100 AND sentiment score <-0.5',
                'Auto-create internal ticket for flagged reviews within 2h',
                'Monthly complaint category trend dashboard with 3-month forecast'
            ],
            'impact'    : 'MEDIUM — surfaces highest-damage complaints before they accumulate'
        }
    ]

    priority_style = {
        'CRITICAL': ('rec-priority-critical', RED),
        'HIGH'    : ('rec-priority-high', AMBER),
        'MEDIUM'  : ('rec-priority-medium', OLA_YELLOW)
    }

    for rec in recs:
        css_class, color = priority_style[rec['priority']]
        actions_html = ''.join([
            f'<div style="font-size:0.82rem; margin:0.3rem 0; color:{TEXT_WHITE};">→ {a}</div>'
            for a in rec['actions']
        ])
        st.markdown(f"""
        <div class="rec-card {css_class}">
            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.6rem;'>
                <div>
                    <span style='font-family:Rajdhani; font-size:1.1rem;
                                 font-weight:700; color:{TEXT_WHITE};'>
                        {rec['title']}
                    </span><br>
                    <span style='font-size:0.72rem; color:{TEXT_MUTED};'>
                        Category: {rec['category']} &nbsp;|&nbsp; Owner: {rec['owner']}
                    </span>
                </div>
                <span class="insight-pill" style='background:rgba(0,0,0,0.3);
                      border-color:{color}; color:{color}; white-space:nowrap;'>
                    {rec['priority']}
                </span>
            </div>
            <div style='font-size:0.78rem; color:{TEXT_MUTED}; margin-bottom:0.6rem;'>
                <b style='color:{OLA_YELLOW};'>Evidence:</b> {rec['evidence']}
            </div>
            {actions_html}
            <div style='margin-top:0.6rem; font-size:0.78rem;
                        color:{color}; font-weight:500;'>
                Expected Impact: {rec['impact']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # KPI tracking table
    st.markdown('<div class="section-header">Recovery KPI Tracker</div>', unsafe_allow_html=True)

    overall_avg = dff['score'].mean()
    one_star_pct = (dff['score'] == 1).mean() * 100
    app_pct = dff['cat_software_app'].mean() * 100
    cc_1star = (dff[dff['cat_customer_care']==True]['score'] == 1).mean() * 100
    multi_pct = (dff['complaint_count'] >= 2).mean() * 100
    avg_sent = dff['sentiment_score'].mean()

    kpi_df = pd.DataFrame([
        ["Overall Avg Star Rating",       f"{overall_avg:.2f}",  "3.5+",   "12 months"],
        ["% 1-Star Reviews",              f"{one_star_pct:.1f}%","<35%",   "12 months"],
        ["Software/App Complaint Rate",   f"{app_pct:.1f}%",     "<25%",   "6 months" ],
        ["Customer Care 1-Star Rate",     f"{cc_1star:.1f}%",    "<70%",   "9 months" ],
        ["Developer Response Rate",       "0.0%",                "40%+",   "3 months" ],
        ["Avg Sentiment Score",           f"{avg_sent:.3f}",     ">0.10",  "12 months"],
        ["Multi-complaint Review Rate",   f"{multi_pct:.1f}%",   "<15%",   "12 months"],
    ], columns=["KPI", "Current", "Target", "Timeframe"])

    st.dataframe(kpi_df, use_container_width=True, hide_index=True)

# =============================================================================
# PAGE 6 — CASE STUDY
# =============================================================================
elif page == "📋 Case Study":

    st.markdown('<div class="page-title">CASE STUDY</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">How did customer perception change and what drove it?</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ola-card" style='margin-bottom:1.5rem; border-color:#333;'>
        <span style='font-size:0.75rem; color:{TEXT_MUTED};'>
        <b style='color:{OLA_YELLOW};'>Editorial note:</b>
        This case study focuses on customer voice and operational evidence from
        {len(df):,} reviews. Corporate events are included as verified public context only.
        This dashboard does not attribute causes to corporate decisions.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Section 1 — Vision
    st.markdown('<div class="section-header">01 · The Vision</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ola-card ola-card-accent">
        <p style='font-size:0.95rem; line-height:1.8; color:{TEXT_WHITE};'>
        OLA Electric entered the Indian EV market with the ambition of accelerating
        electric mobility through software-driven scooters and vertically integrated
        manufacturing. Founded in 2017, the company delivered its first scooter —
        the S1 Pro — in December 2021, positioning itself as a technology-first
        alternative to incumbent two-wheeler manufacturers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Founded",             "2017")
    c2.metric("First Delivery",      "Dec 2021")
    c3.metric("IPO Size",            "₹6,154 Cr")
    c4.metric("IPO Listing",         "Aug 9, 2024")

    # Section 2 — Growth Arc
    st.markdown('<div class="section-header">02 · Growth Arc</div>', unsafe_allow_html=True)

    yearly = df.groupby(df['at'].dt.year).agg(
        reviews=('reviewId','count'),
        avg_rating=('score','mean')
    ).reset_index()
    yearly.columns = ['Year','Reviews','Avg Rating']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly['Year'].astype(str),
        y=yearly['Reviews'],
        name='Review Volume',
        marker_color=OLA_YELLOW,
        opacity=0.8
    ))
    fig.add_trace(go.Scatter(
        x=yearly['Year'].astype(str),
        y=yearly['Avg Rating'],
        name='Avg Rating',
        yaxis='y2',
        line=dict(color=RED, width=3),
        mode='lines+markers',
        marker=dict(size=10)
    ))
    fig.update_layout(
        title="Annual Review Volume vs Average Rating",
        yaxis=dict(title='Reviews', gridcolor='#1E1E1E'),
        yaxis2=dict(title='Avg Rating', overlaying='y', side='right',
                   range=[1,5], gridcolor='#1E1E1E'),
        **PLOT_LAYOUT,
        legend=dict(orientation='h', y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Section 3 — Warning Signs
    st.markdown('<div class="section-header">03 · Warning Signs</div>', unsafe_allow_html=True)

    timeline_events = [
        ("Aug 2, 2024",  "IPO Opens",          f"OLA Electric IPO opens at ₹76/share. Raises ₹6,154 crore. Subscribed 4.27×.", "accent"),
        ("Aug 9, 2024",  "IPO Lists",          "Shares list on BSE and NSE. Initial surge followed by sustained decline.", "accent"),
        ("Oct 7, 2024",  "CCPA Notice #1",     "10,644 complaints filed Sep 2023–Aug 2024. CCPA issues first show-cause notice.", "danger"),
        ("Dec 4, 2024",  "CCPA Notice #2",     "CCPA issues second notice seeking additional documents. 15-day response window.", "danger"),
        ("Jul 2025",     "Peak Crisis Volume", "667 reviews in single month — 274% spike from previous month. Highest in dataset.", "danger"),
    ]

    for date, title, detail, style in timeline_events:
        border = 'ola-card-accent' if style == 'accent' else 'ola-card-danger'
        color  = OLA_YELLOW if style == 'accent' else RED
        st.markdown(f"""
        <div class="ola-card {border}" style='display:flex; gap:1rem; align-items:flex-start;'>
            <div style='min-width:90px; font-family:JetBrains Mono;
                        font-size:0.72rem; color:{color}; margin-top:0.1rem;'>
                {date}
            </div>
            <div>
                <div style='font-weight:600; font-size:0.9rem;
                            color:{TEXT_WHITE}; margin-bottom:0.2rem;'>{title}</div>
                <div style='font-size:0.82rem; color:{TEXT_MUTED};'>{detail}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Section 4 — Customer Voice
    st.markdown('<div class="section-header">04 · What Customers Actually Said</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Reviews Analyzed",   f"{len(df):,}")
    s2.metric("% 1-Star",           f"{(df['score']==1).mean()*100:.1f}%")
    s3.metric("Developer Replies",  "0")
    s4.metric("Dominant Complaint", "Software / App")

    st.markdown(f"""
    <div class="ola-card" style='margin-top:1rem;'>
        <div style='display:flex; gap:2rem; flex-wrap:wrap;'>
            <div style='text-align:center; flex:1;'>
                <div style='font-family:Rajdhani; font-size:2.5rem;
                            font-weight:700; color:{OLA_YELLOW};'>50.5%</div>
                <div style='font-size:0.78rem; color:{TEXT_MUTED};'>of reviews mention app issues</div>
            </div>
            <div style='text-align:center; flex:1;'>
                <div style='font-family:Rajdhani; font-size:2.5rem;
                            font-weight:700; color:{RED};'>93.9%</div>
                <div style='font-size:0.78rem; color:{TEXT_MUTED};'>1-star rate for customer care</div>
            </div>
            <div style='text-align:center; flex:1;'>
                <div style='font-family:Rajdhani; font-size:2.5rem;
                            font-weight:700; color:{AMBER};'>25.5%</div>
                <div style='font-size:0.78rem; color:{TEXT_MUTED};'>reviews mention 2+ problems</div>
            </div>
            <div style='text-align:center; flex:1;'>
                <div style='font-family:Rajdhani; font-size:2.5rem;
                            font-weight:700; color:{TEXT_MUTED};'>0%</div>
                <div style='font-size:0.78rem; color:{TEXT_MUTED};'>developer reply rate — 4 years</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =============================================================================
# Section 5 — Root Cause Analysis
# =============================================================================

st.markdown(
    '<div class="section-header">05 · Root Cause Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="ola-card ola-card-accent">
<div style="font-size:0.9rem; line-height:1.7; color:{TEXT_WHITE};">
Rather than treating every complaint independently, the review corpus suggests
that multiple customer frustrations originate from a single operational bottleneck.
The categories reinforce one another and form a cascading failure rather than isolated issues.
</div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Top operational pain points
# -----------------------------

st.markdown("#### Dominant Operational Failures")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="ola-card" style="text-align:center;">
        <div style="font-size:1rem;font-weight:700;color:{OLA_YELLOW};">
        Software / App
        </div>
        <div style="font-size:2rem;font-weight:700;color:{OLA_YELLOW};">
        50.5%
        </div>
        <div style="font-size:0.75rem;color:{TEXT_MUTED};">
        of reviews
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="ola-card" style="text-align:center;">
        <div style="font-size:1rem;font-weight:700;color:{RED};">
        Customer Care
        </div>
        <div style="font-size:2rem;font-weight:700;color:{RED};">
        93.9%
        </div>
        <div style="font-size:0.75rem;color:{TEXT_MUTED};">
        1-Star Rate
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="ola-card" style="text-align:center;">
        <div style="font-size:1rem;font-weight:700;color:{AMBER};">
        Service Center
        </div>
        <div style="font-size:2rem;font-weight:700;color:{AMBER};">
        88.7%
        </div>
        <div style="font-size:0.75rem;color:{TEXT_MUTED};">
        1-Star Rate
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="ola-card" style="text-align:center;">
        <div style="font-size:1rem;font-weight:700;color:{GREEN};">
        Spare Parts
        </div>
        <div style="font-size:2rem;font-weight:700;color:{GREEN};">
        -0.385
        </div>
        <div style="font-size:0.75rem;color:{TEXT_MUTED};">
        Avg Sentiment
        </div>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# -----------------------------
# Root Cause Chain
# -----------------------------

st.markdown("#### Root Cause Chain")

chain = [
    ("🚀", "Aggressive Sales Growth (2022–2024)", OLA_YELLOW),
    ("🏭", "Service Infrastructure Did Not Scale", OLA_YELLOW),
    ("🔧", "Repair Backlogs & Spare Part Shortages", AMBER),
    ("📞", "Customer Care Became Overloaded", AMBER),
    ("📱", "App Could Not Provide Visibility", AMBER),
    ("⭐", "Customers Shifted To Public Reviews", RED),
    ("📉", "Ratings Fell & Brand Trust Declined", RED),
    ("⚠️", "Market Share Dropped\n38.83% → 17.35%", RED)
]

for i, (icon, text, color) in enumerate(chain):

    st.markdown(
        f"""
        <div style="
            background:{BG_CARD};
            border-left:4px solid {color};
            border-radius:8px;
            padding:14px;
            margin-bottom:6px;
        ">
            <span style="font-size:1.1rem;">{icon}</span>
            <span style="
                font-size:0.95rem;
                color:{TEXT_WHITE};
                margin-left:10px;
                font-weight:500;
            ">
            {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if i != len(chain)-1:
        st.markdown(
            "<div style='text-align:center;font-size:22px;color:#555;'>⬇</div>",
            unsafe_allow_html=True
        )

st.divider()

# -----------------------------
# Executive Insight
# -----------------------------

st.markdown(f"""
<div class="ola-card ola-card-danger">

<span class="insight-pill insight-pill-red">
KEY BUSINESS INSIGHT
</span>

<br><br>

<div style="font-size:0.92rem;line-height:1.8;">

The review corpus suggests that <b>Software</b>, <b>Customer Care</b>,
<b>Service Centers</b>, and <b>Spare Parts</b> should not be treated as
independent operational failures.

They appear to be downstream consequences of one structural issue:

<b>OLA Electric expanded customer acquisition faster than its service
capacity.</b>

Customers initially experienced service delays, followed by communication
breakdowns, lack of spare parts, and poor application visibility.
Unable to resolve issues through official support channels, many customers
moved to public review platforms, accelerating reputation loss.

</div>

</div>
""", unsafe_allow_html=True)