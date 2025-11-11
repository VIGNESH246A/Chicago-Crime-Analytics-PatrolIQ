"""
PatrolIQ - Geographic Crime Heatmaps
------------------------------------
Interactive geographic visualizations with stunning modern design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ======================================================
# PATHS
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH_01 = BASE_DIR / "data" / "processed" / "sample_250000_rows_01.csv"
DATA_PATH_02 = BASE_DIR / "data" / "processed" / "sample_250000_rows_02.csv"
CENTERS_PATH = BASE_DIR / "reports" / "summaries" / "kmeans_geo_centers_k9.csv"

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="🗺️ Geographic Heatmaps", 
    page_icon="🗺️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS - STUNNING MODERN DESIGN
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Montserrat:wght@700;800;900&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Container styling */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1500px;
    }
    
    /* Animated gradient hero title */
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
        margin-bottom: 0.5rem;
        letter-spacing: -3.5px;
        font-family: 'Montserrat', sans-serif;
        text-shadow: 0 0 50px rgba(102, 126, 234, 0.3);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.35rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 3rem;
        animation: fadeInUp 1.3s ease-out;
        letter-spacing: 0.8px;
    }
    
    /* Gradient animation */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
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
            transform: translateX(-35px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleUp {
        0% {
            opacity: 0;
            transform: scale(0.92);
        }
        50% {
            transform: scale(1.02);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Modern tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px;
        border-radius: 22px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 0 32px;
        font-weight: 700;
        font-size: 15px;
        color: #475569;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
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
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Glowing metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 2.2rem 1.8rem;
        border-radius: 24px;
        position: relative;
        transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        animation: scaleUp 0.8s ease-out;
        border: 2px solid #f1f5f9;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.12), transparent);
        transform: rotate(45deg);
        transition: all 0.7s ease;
    }
    
    div[data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    div[data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 24px;
        padding: 2px;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: 0;
        transition: opacity 0.45s ease;
    }
    
    div[data-testid="metric-container"]:hover::after {
        opacity: 1;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-12px) scale(1.04);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.25);
        border-color: transparent;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Montserrat', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.88rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Section headers */
    h1 {
        color: #0f172a;
        font-weight: 800;
        margin-top: 2.5rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.4rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        position: relative;
        padding-bottom: 1.2rem;
        animation: slideInLeft 1s ease-out;
        font-family: 'Montserrat', sans-serif;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 120px;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 3px;
        animation: expandWidth 1.2s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 120px; }
    }
    
    h3 {
        color: #334155;
        font-weight: 700;
        font-size: 1.65rem;
        margin-top: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 2px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #667eea;
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
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.15);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Date input styling */
    .stDateInput > div > div {
        background: white;
        border-radius: 14px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stDateInput > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.15);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 20px;
        border: none;
        padding: 1.4rem 1.8rem;
        animation: scaleUp 0.7s ease-out;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        font-weight: 500;
    }
    
    [data-testid="stInfo"] {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        color: #1e40af;
        border-left: 6px solid #3b82f6;
    }
    
    [data-testid="stSuccess"] {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065f46;
        border-left: 6px solid #10b981;
    }
    
    [data-testid="stWarning"] {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #92400e;
        border-left: 6px solid #f59e0b;
    }
    
    /* Plotly chart styling */
    .js-plotly-plot {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.45s ease;
        animation: scaleUp 0.9s ease-out;
        border: 1px solid #f1f5f9;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
        border: 2px solid #f1f5f9;
        animation: scaleUp 0.8s ease-out;
    }
    
    /* Divider */
    hr {
        margin: 4rem 0;
        border: none;
        height: 4px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #f093fb, transparent);
        border-radius: 2px;
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
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Stats card */
    .stats-card {
        background: white;
        padding: 2rem;
        border-radius: 22px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
        border: 2px solid #f1f5f9;
        transition: all 0.4s ease;
        animation: slideInLeft 0.9s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .stats-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2, #f093fb);
    }
    
    .stats-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown('<h1 class="hero-title">🗺️ Geographic Intelligence Center</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">📍 Interactive Crime Density & Hotspot Visualization Across Chicago</p>', unsafe_allow_html=True)

# ======================================================
# DATA LOADERS
# ======================================================
@st.cache_data
def load_data():
    """Load and combine crime data from both files"""
    df_01 = pd.read_csv(DATA_PATH_01, low_memory=False)
    df_02 = pd.read_csv(DATA_PATH_02, low_memory=False)
    df = pd.concat([df_01, df_02], ignore_index=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Latitude', 'Longitude', 'Date'])
    return df

@st.cache_data
def load_cluster_centers():
    """Load K-Means cluster centers"""
    if CENTERS_PATH.exists():
        return pd.read_csv(CENTERS_PATH)
    return None

# ======================================================
# LOAD DATA
# ======================================================
with st.spinner("🔄 Loading crime data..."):
    df = load_data()
    centers = load_cluster_centers()

st.success(f"✅ Successfully loaded **{len(df):,}** crime records")

# ======================================================
# SIDEBAR FILTERS
# ======================================================
st.sidebar.markdown("## 🔍 Filter Controls")
st.sidebar.markdown("---")

# Date range filter
st.sidebar.subheader("📅 Date Range")
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input(
    "Select Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Crime type filter
st.sidebar.subheader("🚨 Crime Type")
crime_types = ['All'] + sorted(df['Primary Type'].unique().tolist())
selected_crime = st.sidebar.selectbox("Filter by Type", crime_types)

# Sample size slider
st.sidebar.subheader("⚡ Performance")
sample_size = st.sidebar.slider(
    "Sample Size",
    min_value=1000,
    max_value=100000,
    value=50000,
    step=1000,
    help="Adjust for better performance"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Lower sample size = faster rendering")

# ======================================================
# APPLY FILTERS
# ======================================================
filtered_df = df.copy()

# Date filter
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= date_range[0]) &
        (filtered_df['Date'].dt.date <= date_range[1])
    ]

# Crime type filter
if selected_crime != 'All':
    filtered_df = filtered_df[filtered_df['Primary Type'] == selected_crime]

# Sample for visualization
viz_df = filtered_df.sample(n=min(sample_size, len(filtered_df)), random_state=42)

# ======================================================
# FILTER SUMMARY
# ======================================================
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.metric("📊 Total Filtered", f"{len(filtered_df):,}", delta=None)

with col2:
    st.metric("👁️ Displaying", f"{len(viz_df):,}", delta=None)

with col3:
    reduction = ((len(filtered_df) - len(viz_df)) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("💾 Data Reduction", f"{reduction:.1f}%", delta=None)

st.markdown("---")

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔥 Density Heatmap",
    "📍 Crime Scatter Plot",
    "🎯 Hotspot Centers",
    "📊 Statistical Summary"
])

# ======================================================
# TAB 1: DENSITY HEATMAP
# ======================================================
with tab1:
    st.header("🔥 Crime Density Heatmap")
    st.markdown("Visualize crime concentration across Chicago neighborhoods")
    
    # Density heatmap
    fig = px.density_mapbox(
        viz_df,
        lat='Latitude',
        lon='Longitude',
        radius=12,
        zoom=10,
        center={"lat": 41.8781, "lon": -87.6298},
        mapbox_style="open-street-map",
        title="High-Resolution Crime Density Map",
        hover_data=['Primary Type', 'Date'],
        color_continuous_scale='Inferno'
    )
    
    fig.update_layout(
        height=750,
        margin={"r":0,"t":50,"l":0,"b":0},
        font=dict(family="Inter, sans-serif", size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("🔍 **Darker areas** indicate higher crime density. Zoom in for detailed neighborhood analysis.")

# ======================================================
# TAB 2: SCATTER PLOT
# ======================================================
with tab2:
    st.header("📍 Crime Location Scatter Plot")
    st.markdown("Individual crime incidents colored by type")
    
    # Color by crime type
    fig = px.scatter_mapbox(
        viz_df,
        lat='Latitude',
        lon='Longitude',
        color='Primary Type',
        zoom=10,
        center={"lat": 41.8781, "lon": -87.6298},
        mapbox_style="open-street-map",
        title="Crime Locations by Type",
        hover_data=['Primary Type', 'Date', 'Location Description'],
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        height=750,
        margin={"r":0,"t":50,"l":0,"b":0},
        font=dict(family="Inter, sans-serif", size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top crime types
    st.subheader("📈 Top Crime Types in Selection")
    top_crimes = viz_df['Primary Type'].value_counts().head(10)
    
    fig_bar = px.bar(
        x=top_crimes.values,
        y=top_crimes.index,
        orientation='h',
        title="Most Frequent Crime Types",
        labels={'x': 'Count', 'y': 'Crime Type'},
        color=top_crimes.values,
        color_continuous_scale='Purples'
    )
    
    fig_bar.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

# ======================================================
# TAB 3: CLUSTER CENTERS
# ======================================================
with tab3:
    st.header("🎯 K-Means Hotspot Centers")
    st.markdown("9 major crime hotspots identified by clustering algorithm")
    
    if centers is not None:
        # Create map with cluster centers
        fig = go.Figure()
        
        # Add crime points (background)
        fig.add_trace(go.Scattermapbox(
            lat=viz_df['Latitude'],
            lon=viz_df['Longitude'],
            mode='markers',
            marker=dict(size=4, color='lightblue', opacity=0.4),
            name='Crime Locations',
            hoverinfo='skip'
        ))
        
        # Add cluster centers (foreground)
        fig.add_trace(go.Scattermapbox(
            lat=centers['Latitude'],
            lon=centers['Longitude'],
            mode='markers+text',
            marker=dict(size=28, color='#667eea', symbol='star'),
            text=[f"Hotspot {i+1}" for i in range(len(centers))],
            textposition="top center",
            textfont=dict(size=16, color='#1e293b', family='Montserrat'),
            name='Hotspot Centers',
            hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
        ))
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center={"lat": 41.8781, "lon": -87.6298},
                zoom=10
            ),
            height=750,
            margin={"r":0,"t":50,"l":0,"b":0},
            title="9 Geographic Crime Hotspots (K-Means Clustering)",
            font=dict(family="Inter, sans-serif", size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display coordinates
        st.subheader("📍 Hotspot Coordinates")
        centers_display = centers.copy()
        centers_display.index = [f"⭐ Hotspot {i+1}" for i in range(len(centers))]
        st.dataframe(centers_display, use_container_width=True)
        
        st.success("✅ These 9 hotspots represent the highest crime concentration areas in Chicago")
    else:
        st.warning("⚠️ Cluster centers not found. Please run `geo_clustering.py` first.")

# ======================================================
# TAB 4: STATISTICS
# ======================================================
with tab4:
    st.header("📊 Geographic Statistics & Insights")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚨 Total Crimes", f"{len(filtered_df):,}")
    
    with col2:
        if len(filtered_df) > 0:
            most_common = filtered_df['Primary Type'].mode()[0]
            st.metric("🎯 Top Crime Type", most_common)
        else:
            st.metric("🎯 Top Crime Type", "N/A")
    
    with col3:
        if 'Community Area' in filtered_df.columns and len(filtered_df) > 0:
            top_area = filtered_df['Community Area'].mode()[0]
            st.metric("📍 Top Area", f"#{int(top_area)}")
        else:
            st.metric("📍 Top Area", "N/A")
    
    with col4:
        if 'Arrest' in filtered_df.columns and len(filtered_df) > 0:
            arrest_rate = (filtered_df['Arrest'].sum() / len(filtered_df)) * 100
            st.metric("⚖️ Arrest Rate", f"{arrest_rate:.1f}%")
        else:
            st.metric("⚖️ Arrest Rate", "N/A")
    
    st.markdown("---")
    
    # Crime distribution by location
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Top Crime Locations")
        if 'Location Description' in filtered_df.columns:
            top_locations = filtered_df['Location Description'].value_counts().head(10)
            
            fig_loc = px.bar(
                y=top_locations.index,
                x=top_locations.values,
                orientation='h',
                title="Most Common Crime Locations",
                labels={'x': 'Crimes', 'y': 'Location'},
                color=top_locations.values,
                color_continuous_scale='Viridis'
            )
            
            fig_loc.update_layout(
                height=450,
                font=dict(family="Inter, sans-serif")
            )
            
            st.plotly_chart(fig_loc, use_container_width=True)
    
    with col2:
        st.subheader("🏘️ Crime by Community Area")
        if 'Community Area' in filtered_df.columns:
            area_counts = filtered_df['Community Area'].value_counts().head(10)
            
            fig_area = px.bar(
                y=[f"Area {int(x)}" for x in area_counts.index],
                x=area_counts.values,
                orientation='h',
                title="Highest Crime Community Areas",
                labels={'x': 'Crimes', 'y': 'Area'},
                color=area_counts.values,
                color_continuous_scale='Reds'
            )
            
            fig_area.update_layout(
                height=450,
                font=dict(family="Inter, sans-serif")
            )
            
            st.plotly_chart(fig_area, use_container_width=True)
    
    # Time-based analysis
    st.markdown("---")
    st.subheader("⏰ Temporal Distribution")
    
    # Crime by hour
    hourly_data = filtered_df.copy()
    hourly_data['Hour'] = hourly_data['Date'].dt.hour
    hourly_counts = hourly_data['Hour'].value_counts().sort_index()
    
    fig_hourly = px.line(
        x=hourly_counts.index,
        y=hourly_counts.values,
        markers=True,
        title="Crime Frequency by Hour of Day",
        labels={'x': 'Hour', 'y': 'Number of Crimes'}
    )
    
    fig_hourly.update_traces(
        line_color='#667eea',
        marker=dict(size=10, color='#764ba2')
    )
    
    fig_hourly.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif"),
        xaxis_title="Hour of Day",
        yaxis_title="Crime Count"
    )
    
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Key insights
    st.markdown("---")
    st.subheader("💡 Key Geographic Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3 style="color: #667eea; margin-top: 0;">🗺️ Spatial Patterns</h3>
            <ul style="line-height: 2; color: #475569;">
                <li>Crime concentrates in <strong>9 major hotspots</strong></li>
                <li>Dense urban areas show higher incident rates</li>
                <li>Cluster patterns reveal systematic targeting</li>
                <li>Geographic spread indicates patrol optimization needs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3 style="color: #764ba2; margin-top: 0;">📈 Actionable Intelligence</h3>
            <ul style="line-height: 2; color: #475569;">
                <li>Focus resources on identified hotspot centers</li>
                <li>Monitor temporal patterns at high-density locations</li>
                <li>Cross-reference with community demographics</li>
                <li>Deploy predictive models for proactive policing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# FOOTER SUMMARY
# ======================================================
st.markdown("---")
st.markdown("### 🎯 Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.info(f"""
    **📊 Data Coverage**
    - Total Records: {len(df):,}
    - Filtered: {len(filtered_df):,}
    - Displayed: {len(viz_df):,}
    """)

with summary_col2:
    if len(filtered_df) > 0:
        date_span = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
        st.info(f"""
        **📅 Time Span**
        - From: {filtered_df['Date'].min().strftime('%Y-%m-%d')}
        - To: {filtered_df['Date'].max().strftime('%Y-%m-%d')}
        - Days: {date_span}
        """)
    else:
        st.info("**📅 Time Span**\nNo data in selection")

with summary_col3:
    st.info(f"""
    **🎯 Clustering Info**
    - Method: K-Means
    - Clusters: 9 Hotspots
    - Status: {'✅ Loaded' if centers is not None else '⚠️ Not Found'}
    """)

st.success("✅ Geographic analysis complete! Use filters to explore different crime patterns and hotspot distributions.")