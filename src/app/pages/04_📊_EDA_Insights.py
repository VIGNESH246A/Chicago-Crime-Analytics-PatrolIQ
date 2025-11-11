"""
PatrolIQ - Exploratory Data Analysis (EDA) Insights
----------------------------------------------------
Display comprehensive EDA results and statistical summaries with modern design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import streamlit.components.v1 as components

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH_01 = BASE_DIR / "data" / "processed" / "sample_250000_rows_01.csv"
DATA_PATH_02 = BASE_DIR / "data" / "processed" / "sample_250000_rows_02.csv"
FIG_DIR = BASE_DIR / "reports" / "figures"
SUM_DIR = BASE_DIR / "reports" / "summaries"

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="📊 PatrolIQ EDA", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# ======================================================
# CUSTOM CSS - MODERN VIBRANT DESIGN
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Container styling */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1450px;
    }
    
    /* Animated gradient title */
    .hero-title {
        font-size: 4.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 12s ease infinite;
        margin-bottom: 0.4rem;
        letter-spacing: -3.5px;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.35rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 3rem;
        animation: fadeInUp 1.2s ease-out;
        letter-spacing: 0.3px;
    }
    
    /* Gradient animation */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        25% { background-position: 50% 50%; }
        50% { background-position: 100% 50%; }
        75% { background-position: 50% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(35px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.85);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Modern tab design with glow effect */
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px;
        border-radius: 18px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 14px;
        padding: 0 32px;
        font-weight: 700;
        font-size: 15px;
        color: #64748b;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: left 0.4s ease;
        z-index: -1;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.25);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid #667eea !important;
        color: white !important;
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Neon glow metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        position: relative;
        transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        animation: zoomIn 0.7s ease-out;
        border: 2px solid #f1f5f9;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    div[data-testid="metric-container"]:hover::before {
        opacity: 1;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.04);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.25);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.88rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Headers with gradient underline */
    h1 {
        color: #1e293b;
        font-weight: 800;
        margin-top: 2rem;
    }
    
    h2 {
        color: #334155;
        font-weight: 800;
        font-size: 2.4rem;
        margin-top: 2.8rem;
        margin-bottom: 1.8rem;
        position: relative;
        padding-bottom: 1rem;
        animation: slideInLeft 0.9s ease-out;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 90px;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 3px;
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 90px; }
    }
    
    h3 {
        color: #475569;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 1.8rem;
    }
    
    /* Vibrant alert boxes */
    .stAlert {
        border-radius: 18px;
        border: none;
        padding: 1.4rem 1.7rem;
        animation: zoomIn 0.6s ease-out;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        font-weight: 500;
    }
    
    [data-testid="stInfo"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        border-left: 6px solid #3b82f6;
    }
    
    [data-testid="stSuccess"] {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border-left: 6px solid #10b981;
    }
    
    [data-testid="stWarning"] {
        background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        color: #92400e;
        border-left: 6px solid #f97316;
    }
    
    /* Plotly chart styling */
    .js-plotly-plot {
        border-radius: 22px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.45s ease;
        animation: zoomIn 0.8s ease-out;
        border: 1px solid #f1f5f9;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid #f1f5f9;
    }
    
    /* Divider */
    hr {
        margin: 3.5rem 0;
        border: none;
        height: 4px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #f093fb, transparent);
        border-radius: 2px;
    }
    
    /* Insight cards with animation */
    .insight-box {
        background: white;
        padding: 2rem;
        border-radius: 22px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
        border: 2px solid #f8fafc;
        transition: all 0.45s ease;
        animation: slideInLeft 0.9s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .insight-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2, #f093fb);
    }
    
    .insight-box:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .insight-box strong {
        font-size: 1.25rem;
        color: #1e293b;
        display: block;
        margin-bottom: 1rem;
    }
    
    .insight-box ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .insight-box li {
        padding: 0.65rem 0;
        color: #475569;
        font-size: 1rem;
        position: relative;
        padding-left: 2rem;
    }
    
    .insight-box li::before {
        content: '◆';
        position: absolute;
        left: 0;
        color: #667eea;
        font-size: 1.3rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f8fafc;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
        border: 3px solid #f8fafc;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.9rem 2.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.45);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: white;
        border-radius: 14px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: white;
        border-radius: 14px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown('<h1 class="hero-title">📊 EDA Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🔍 Deep Statistical Analysis & Visual Exploration of Chicago Crime Patterns</p>', unsafe_allow_html=True)

# ======================================================
# DATA LOADERS
# ======================================================
@st.cache_data
def load_summary_csv(filename):
    path = SUM_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_data():
    if DATA_PATH_01.exists() and DATA_PATH_02.exists():
        df_01 = pd.read_csv(DATA_PATH_01, low_memory=False)
        df_02 = pd.read_csv(DATA_PATH_02, low_memory=False)
        df = pd.concat([df_01, df_02], ignore_index=True)
        df['Date'] = pd.to_datetime(df.get('Date'), errors='coerce')
        df = df.dropna(subset=['Date'])
        return df
    return None

def display_image(image_path):
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.warning(f"⚠️ Image not found: {image_path.name}")

def display_html(html_path):
    if html_path.exists():
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except UnicodeDecodeError:
            try:
                with open(html_path, 'r', encoding='latin-1') as f:
                    html_content = f.read()
            except Exception as e:
                st.error(f"❌ Error reading HTML file: {e}")
                return
        
        components.html(html_content, height=600, scrolling=True)
    else:
        st.warning(f"⚠️ HTML file not found: {html_path.name}")

# Load data
df = load_data()

if df is not None:
    st.success(f"✅ Loaded {len(df):,} crime records for comprehensive analysis")
else:
    st.error("❌ Data not found. Please run eda_pipeline.py first.")
    st.stop()

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔢 Crime Distribution",
    "🗺️ Geographic Patterns",
    "⏰ Temporal Trends",
    "👮 Arrest Analysis",
    "📈 Statistical Summary",
    "🏘️ Community Analysis"
])

# ======================================================
# TAB 1: CRIME DISTRIBUTION
# ======================================================
with tab1:
    st.header("🔢 Crime Type Distribution Analysis")
    
    crime_counts = load_summary_csv("crime_counts.csv")
    
    if crime_counts is not None:
        crime_counts.columns = ['Primary Type', 'Count']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Top 20 Crime Types")
            
            fig = px.bar(
                crime_counts.head(20),
                x='Primary Type',
                y='Count',
                title="Crime Type Frequency Distribution",
                color='Count',
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=520,
                showlegend=False,
                font=dict(family="Inter, sans-serif")
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥇 Top 10 Crimes")
            top_10 = crime_counts.head(10)
            
            for i, row in top_10.iterrows():
                st.metric(
                    f"{i+1}. {row['Primary Type'][:20]}",
                    f"{row['Count']:,}",
                    delta=f"{(row['Count']/crime_counts['Count'].sum()*100):.1f}%"
                )
        
        st.markdown("---")
        st.subheader("📈 Static Visualization")
        display_image(FIG_DIR / "top20_crime_types.png")
        
        st.markdown("---")
        st.subheader("🔍 Interactive Full Distribution")
        display_html(FIG_DIR / "crime_type_distribution.html")
        
        st.markdown("---")
        st.subheader("📊 Crime Type Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Crime Types", len(crime_counts))
        
        with col2:
            most_common = crime_counts.iloc[0]
            st.metric("Most Common", most_common['Primary Type'][:15])
        
        with col3:
            top_3_pct = (crime_counts.head(3)['Count'].sum() / crime_counts['Count'].sum() * 100)
            st.metric("Top 3 Crimes %", f"{top_3_pct:.1f}%")
        
        with col4:
            least_common = crime_counts.iloc[-1]
            st.metric("Least Common", least_common['Primary Type'][:15])
        
        st.download_button(
            label="📥 Download Crime Counts CSV",
            data=crime_counts.to_csv(index=False),
            file_name="crime_counts.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Crime counts data not found")

# ======================================================
# TAB 2: GEOGRAPHIC PATTERNS
# ======================================================
with tab2:
    st.header("🗺️ Geographic Crime Patterns")
    
    st.subheader("🌍 Crime Location Scatter Plot (50K Sample)")
    display_image(FIG_DIR / "geo_scatter_50k.png")
    
    st.markdown("---")
    st.subheader("🔥 Interactive Crime Heatmap")
    display_html(FIG_DIR / "crime_heatmap.html")
    
    st.info("🗺️ The heatmap visualizes crime density across Chicago using 50,000 sampled points")
    
    if df is not None:
        st.markdown("---")
        st.subheader("📍 Geographic Statistics")
        
        latlon_data = df.dropna(subset=['Latitude', 'Longitude'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Records with Coordinates", f"{len(latlon_data):,}")
        
        with col2:
            lat_range = latlon_data['Latitude'].max() - latlon_data['Latitude'].min()
            st.metric("Latitude Range", f"{lat_range:.4f}°")
        
        with col3:
            lon_range = latlon_data['Longitude'].max() - latlon_data['Longitude'].min()
            st.metric("Longitude Range", f"{lon_range:.4f}°")
        
        with col4:
            center_lat = latlon_data['Latitude'].mean()
            st.metric("Center Latitude", f"{center_lat:.4f}°")
        
        st.subheader("📊 Coordinate Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                latlon_data.sample(min(50000, len(latlon_data))),
                x='Latitude',
                nbins=50,
                title="Latitude Distribution",
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                latlon_data.sample(min(50000, len(latlon_data))),
                x='Longitude',
                nbins=50,
                title="Longitude Distribution",
                color_discrete_sequence=['#764ba2']
            )
            fig.update_layout(font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)

# ======================================================
# TAB 3: TEMPORAL TRENDS
# ======================================================
with tab3:
    st.header("⏰ Temporal Crime Patterns")
    
    st.subheader("⏰ Hourly Crime Distribution")
    
    hourly_counts = load_summary_csv("hourly_counts.csv")
    if hourly_counts is not None:
        hourly_counts.columns = ['Hour', 'Count']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.line(
                hourly_counts,
                x='Hour',
                y='Count',
                markers=True,
                title="Crime Frequency by Hour of Day"
            )
            fig.update_traces(line_color='#667eea', line_width=3, marker=dict(size=10, color='#764ba2'))
            fig.update_layout(font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔝 Peak Hours")
            peak_hours = hourly_counts.nlargest(5, 'Count')
            for i, row in peak_hours.iterrows():
                st.metric(
                    f"Hour {row['Hour']}:00",
                    f"{row['Count']:,} crimes"
                )
    
    display_image(FIG_DIR / "crimes_by_hour.png")
    
    st.markdown("---")
    
    st.subheader("🗓️ Weekday × Hour Heatmap")
    display_image(FIG_DIR / "weekday_hour_heatmap.png")
    
    hour_week = load_summary_csv("hour_week_counts.csv")
    if hour_week is not None:
        st.info("📊 This heatmap reveals crime patterns across hours and weekdays")
    
    st.markdown("---")
    
    st.subheader("📅 Monthly Crime Trends by Year")
    display_html(FIG_DIR / "monthly_trend_by_year.html")
    
    monthly_trend = load_summary_csv("monthly_trend.csv")
    if monthly_trend is not None:
        monthly_trend = monthly_trend.loc[:, ~monthly_trend.columns.str.contains('^Unnamed')]
        st.dataframe(monthly_trend.head(20), use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🌍 Seasonal Crime Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_image(FIG_DIR / "crimes_by_season.png")
    
    with col2:
        season_counts = load_summary_csv("season_counts.csv")
        if season_counts is not None:
            season_counts.columns = ['Season', 'Count']
            st.subheader("📊 Season Statistics")
            
            for i, row in season_counts.iterrows():
                emoji = {'Winter': '❄️', 'Spring': '🌸', 'Summer': '☀️', 'Fall': '🍂'}
                st.metric(
                    f"{emoji.get(row['Season'], '🌍')} {row['Season']}",
                    f"{row['Count']:,}"
                )

# ======================================================
# TAB 4: ARREST ANALYSIS
# ======================================================
with tab4:
    st.header("👮 Arrest Rate & Domestic Incident Analysis")
    
    arrest_dom = load_summary_csv("arrest_domestic_by_type.csv")
    
    if arrest_dom is not None:
        st.subheader("📊 Arrest Rates by Crime Type")
        
        display_image(FIG_DIR / "arrest_rate_by_type_top15.png")
        
        st.markdown("---")
        
        st.subheader("🔍 Detailed Arrest & Domestic Analysis")
        
        sort_by = st.selectbox(
            "Sort by",
            ['Total Crimes', 'Arrest Rate', 'Domestic Rate'],
            key='arrest_sort'
        )
        
        sort_col_map = {
            'Total Crimes': 'total',
            'Arrest Rate': 'arrest_rate',
            'Domestic Rate': 'domestic_rate'
        }
        
        sorted_df = arrest_dom.sort_values(sort_col_map[sort_by], ascending=False).head(20)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                sorted_df,
                x='Primary Type',
                y='arrest_rate',
                title="Arrest Rate by Crime Type (Top 20)",
                color='arrest_rate',
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
            )
            fig.update_layout(xaxis_tickangle=-45, height=500, font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                sorted_df,
                x='Primary Type',
                y='domestic_rate',
                title="Domestic Incident Rate by Crime Type (Top 20)",
                color='domestic_rate',
                color_continuous_scale=['#f093fb', '#764ba2', '#667eea']
            )
            fig.update_layout(xaxis_tickangle=-45, height=500, font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Full Data Table")
        
        display_df = arrest_dom.copy()
        display_df['arrest_rate'] = (display_df['arrest_rate'] * 100).round(2)
        display_df['domestic_rate'] = (display_df['domestic_rate'] * 100).round(2)
        
        st.dataframe(
            display_df.style.background_gradient(subset=['arrest_rate'], cmap='Blues')
                           .background_gradient(subset=['domestic_rate'], cmap='Purples')
                           .format({'arrest_rate': '{:.2f}%', 'domestic_rate': '{:.2f}%'}),
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        st.subheader("💡 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            highest_arrest = arrest_dom.loc[arrest_dom['arrest_rate'].idxmax()]
            st.metric(
                "Highest Arrest Rate",
                highest_arrest['Primary Type'][:20],
                f"{highest_arrest['arrest_rate']*100:.1f}%"
            )
        
        with col2:
            lowest_arrest = arrest_dom.loc[arrest_dom['arrest_rate'].idxmin()]
            st.metric(
                "Lowest Arrest Rate",
                lowest_arrest['Primary Type'][:20],
                f"{lowest_arrest['arrest_rate']*100:.1f}%"
            )
        
        with col3:
            avg_arrest = arrest_dom['arrest_rate'].mean()
            st.metric(
                "Average Arrest Rate",
                f"{avg_arrest*100:.1f}%"
            )
        
        st.download_button(
            label="📥 Download Arrest Analysis CSV",
            data=arrest_dom.to_csv(index=False),
            file_name="arrest_domestic_analysis.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Arrest analysis data not found")

# ======================================================
# TAB 5: STATISTICAL SUMMARY
# ======================================================
with tab5:
    st.header("📈 Statistical Summary & Insights")
    
    summary_stats = load_summary_csv("general_summary_stats.csv")
    
    if summary_stats is not None:
        st.subheader("📊 Descriptive Statistics")
        
        st.dataframe(
            summary_stats.style.background_gradient(cmap='RdYlGn_r', axis=1),
            use_container_width=True,
            height=600
        )
        
        st.markdown("---")
        
        st.subheader("🔢 Key Metrics")
        
        if df is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            
            with col2:
                unique_crimes = df['Primary Type'].nunique()
                st.metric("Unique Crime Types", unique_crimes)
            
            with col3:
                if 'District' in df.columns:
                    unique_districts = df['District'].nunique()
                    st.metric("Districts", unique_districts)
            
            with col4:
                if 'Community Area' in df.columns:
                    unique_areas = df['Community Area'].nunique()
                    st.metric("Community Areas", unique_areas)
            
            st.markdown("---")
            st.subheader("📅 Data Coverage")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_date = df['Date'].min()
                st.metric("Start Date", min_date.strftime('%Y-%m-%d'))
            
            with col2:
                max_date = df['Date'].max()
                st.metric("End Date", max_date.strftime('%Y-%m-%d'))
            
            with col3:
                date_range = (max_date - min_date).days
                st.metric("Date Range", f"{date_range:,} days")
            
            st.markdown("---")
            st.subheader("🔍 Data Quality Analysis")
            
            missing_data = df.isnull().sum()
            missing_pct = (missing_data / len(df) * 100).round(2)
            
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing %': missing_pct.values
            })
            missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
            
            if not missing_df.empty:
                fig = px.bar(
                    missing_df.head(15),
                    x='Column',
                    y='Missing %',
                    title="Top 15 Columns with Missing Data",
                    color='Missing %',
                    color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
                )
                fig.update_layout(xaxis_tickangle=-45, height=400, font=dict(family="Inter, sans-serif"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No missing data found!")
        
        st.download_button(
            label="📥 Download Statistical Summary CSV",
            data=summary_stats.to_csv(),
            file_name="statistical_summary.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Statistical summary not found")

# ======================================================
# TAB 6: COMMUNITY ANALYSIS
# ======================================================
with tab6:
    st.header("🏘️ Community Area Analysis")
    
    community_areas = load_summary_csv("top_community_areas.csv")
    
    if community_areas is not None:
        st.subheader("🏘️ Crime Distribution by Community Area")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            top_20 = community_areas.head(20)
            
            fig = px.bar(
                top_20,
                x='Community Area',
                y='counts',
                title="Top 20 Community Areas by Crime Count",
                color='counts',
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
            )
            fig.update_layout(height=500, font=dict(family="Inter, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥇 Top 10 Areas")
            top_10 = community_areas.head(10)
            
            for i, row in top_10.iterrows():
                st.metric(
                    f"#{i+1} Area {int(row['Community Area'])}",
                    f"{row['counts']:,} crimes"
                )
        
        st.markdown("---")
        
        st.subheader("📊 Community Area Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Areas", len(community_areas))
        
        with col2:
            top_area = community_areas.iloc[0]
            st.metric("Highest Crime Area", int(top_area['Community Area']))
        
        with col3:
            top_crime_count = community_areas.iloc[0]['counts']
            st.metric("Highest Crime Count", f"{top_crime_count:,}")
        
        with col4:
            avg_crimes = community_areas['counts'].mean()
            st.metric("Average per Area", f"{avg_crimes:,.0f}")
        
        st.markdown("---")
        st.subheader("📋 All Community Areas Data")
        
        st.dataframe(
            community_areas.style.background_gradient(subset=['counts'], cmap='YlOrRd'),
            use_container_width=True,
            height=400
        )
        
        fig = px.histogram(
            community_areas,
            x='counts',
            nbins=30,
            title="Distribution of Crimes Across Community Areas",
            labels={'counts': 'Crime Count', 'count': 'Number of Areas'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(font=dict(family="Inter, sans-serif"))
        st.plotly_chart(fig, use_container_width=True)
        
        st.download_button(
            label="📥 Download Community Area Data CSV",
            data=community_areas.to_csv(index=False),
            file_name="community_area_analysis.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Community area data not found")
    
    st.markdown("---")
    st.subheader("🔍 Sample Data Preview")
    
    sample_data = load_summary_csv("sample_for_ui.csv")
    if sample_data is not None:
        st.info("📊 Showing 1000 randomly sampled records for detailed exploration")
        st.dataframe(sample_data, use_container_width=True, height=400)
        
        st.download_button(
            label="📥 Download Sample Data CSV",
            data=sample_data.to_csv(index=False),
            file_name="sample_data_1000.csv",
            mime="text/csv"
        )

# ======================================================
# SUMMARY SECTION
# ======================================================
st.markdown("---")
st.subheader("💡 EDA Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="insight-box">
        <strong>🎯 Crime Distribution</strong>
        <ul>
            <li>33 unique crime types identified</li>
            <li>Top 3 crimes dominate the dataset</li>
            <li>Significant frequency variation across types</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
        <strong>🗺️ Geographic Patterns</strong>
        <ul>
            <li>Crimes concentrated in specific hotspots</li>
            <li>Clear density zones identified</li>
            <li>Coordinate-based clustering visible</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="insight-box">
        <strong>⏰ Temporal Patterns</strong>
        <ul>
            <li>Distinct hourly peak periods</li>
            <li>Weekday variations evident</li>
            <li>Seasonal fluctuations present</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.success("✅ EDA analysis complete! Use these insights to inform clustering and predictive modeling strategies.")