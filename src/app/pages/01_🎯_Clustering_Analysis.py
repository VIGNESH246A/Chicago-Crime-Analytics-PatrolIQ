"""
PatrolIQ - Clustering Analysis Dashboard
----------------------------------------
Displays results from Geographic (K-Means, DBSCAN, Hierarchical) and Temporal clustering.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import streamlit.components.v1 as components

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
REPORTS_DIR = BASE_DIR / "reports" / "summaries"
FIGURES_DIR = BASE_DIR / "reports" / "figures"

# Files
GEO_METRICS = REPORTS_DIR / "geo_clustering_metrics.json"
TEMP_METRICS = REPORTS_DIR / "temporal_clustering_metrics.json"
TEMP_SUMMARY = REPORTS_DIR / "temporal_cluster_summary.csv"
CENTERS_PATH = REPORTS_DIR / "kmeans_geo_centers_k9.csv"
MAP_PATH = FIGURES_DIR / "map_dbscan_geo.html"
DENDRO_PATH = FIGURES_DIR / "dendrogram_geo.png"

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="🎯 PatrolIQ Clustering", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# ======================================================
# CUSTOM CSS - CLEAN MODERN DESIGN
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Container styling */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1400px;
    }
    
    /* Animated gradient title */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 8s ease infinite;
        margin-bottom: 0.5rem;
        letter-spacing: -3px;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #6c757d;
        font-weight: 400;
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out;
    }
    
    /* Gradient animation */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
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
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Modern tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background: white;
        border: 2px solid #dee2e6;
        border-radius: 12px 12px 0 0;
        padding: 0 28px;
        font-weight: 600;
        font-size: 15px;
        color: #495057;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #4ECDC4;
        color: #4ECDC4;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%) !important;
        border: 2px solid #4ECDC4 !important;
        color: white !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);
    }
    
    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #4ECDC4, #45B7D1);
    }
    
    /* Metric cards with neon effect */
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.8rem;
        border-radius: 20px;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: scaleIn 0.6s ease-out;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1);
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
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.25);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Headers with modern styling */
    h1 {
        color: #212529;
        font-weight: 700;
        margin-top: 2rem;
    }
    
    h2 {
        color: #343a40;
        font-weight: 700;
        font-size: 2.2rem;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        padding-bottom: 1rem;
        animation: slideIn 0.8s ease-out;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #4ECDC4, #45B7D1);
        border-radius: 2px;
    }
    
    h3 {
        color: #495057;
        font-weight: 600;
        font-size: 1.4rem;
        margin-top: 1.5rem;
    }
    
    /* Info/Alert boxes with modern colors */
    .stAlert {
        border-radius: 16px;
        border: none;
        padding: 1.2rem 1.5rem;
        animation: scaleIn 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    [data-testid="stInfo"] {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #1565C0;
        border-left: 5px solid #2196F3;
    }
    
    [data-testid="stSuccess"] {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        color: #2E7D32;
        border-left: 5px solid #4CAF50;
    }
    
    [data-testid="stWarning"] {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        color: #E65100;
        border-left: 5px solid #FF9800;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: scaleIn 0.7s ease-out;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(78, 205, 196, 0.2);
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    /* Divider */
    hr {
        margin: 3rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #4ECDC4, #45B7D1, transparent);
        border-radius: 2px;
    }
    
    /* Insight cards with shadow effect */
    .insight-box {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid #f8f9fa;
        transition: all 0.4s ease;
        animation: slideIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .insight-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #FF6B6B, #4ECDC4, #45B7D1);
    }
    
    .insight-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(78, 205, 196, 0.2);
        border-color: #4ECDC4;
    }
    
    .insight-box strong {
        font-size: 1.2rem;
        color: #212529;
        display: block;
        margin-bottom: 1rem;
    }
    
    .insight-box ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .insight-box li {
        padding: 0.6rem 0;
        color: #495057;
        font-size: 1rem;
        position: relative;
        padding-left: 1.8rem;
    }
    
    .insight-box li::before {
        content: '✦';
        position: absolute;
        left: 0;
        color: #4ECDC4;
        font-size: 1.2rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4ECDC4, #45B7D1);
        border-radius: 10px;
        border: 2px solid #f8f9fa;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #45B7D1, #4ECDC4);
    }
    
    /* Button-like elements */
    .stButton > button {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown('<h1 class="hero-title">🎯 PatrolIQ Clustering Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🚨 Advanced Geographic & Temporal Crime Pattern Analysis System</p>', unsafe_allow_html=True)

# ======================================================
# DATA LOADERS
# ======================================================
@st.cache_data
def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

@st.cache_data
def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return None

geo_metrics = load_json(GEO_METRICS)
temp_metrics = load_json(TEMP_METRICS)
temp_summary = load_csv(TEMP_SUMMARY)
centers = load_csv(CENTERS_PATH)

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 K-Means Clustering",
    "🔍 DBSCAN Clustering",
    "🌳 Hierarchical Clustering",
    "📊 Performance Comparison"
])

# ======================================================
# TAB 1: K-MEANS
# ======================================================
with tab1:
    st.header("📍 Geographic Hotspots using K-Means")

    if geo_metrics and "kmeans" in geo_metrics:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Silhouette Score", f"{geo_metrics['kmeans']['silhouette']:.4f}")
        with col2:
            st.metric("Davies-Bouldin Index", f"{geo_metrics['kmeans']['davies_bouldin']:.4f}")

        if centers is not None:
            st.subheader("🗺️ Hotspot Map")
            fig = go.Figure()

            fig.add_trace(go.Scattermapbox(
                lat=centers["Latitude"],
                lon=centers["Longitude"],
                mode='markers+text',
                marker=dict(size=22, color='red', symbol='star'),
                text=[f"Hotspot {i+1}" for i in range(len(centers))],
                textposition="top center",
                textfont=dict(size=14, color='black'),
                name='Hotspot Centers',
                hovertemplate="<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>"
            ))

            fig.update_layout(
                mapbox=dict(style="open-street-map", center={"lat": 41.8781, "lon": -87.6298}, zoom=10),
                title="Chicago Crime Hotspots (K-Means)",
                height=600,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Hotspot Center Coordinates")
            st.dataframe(centers.rename_axis("Hotspot"), use_container_width=True)

        st.info("💡 K-Means effectively identifies high-crime density centers (hotspots) across Chicago.")

    else:
        st.warning("⚠️ No K-Means metrics found. Please run `geo_clustering.py` first.")

# ======================================================
# TAB 2: DBSCAN
# ======================================================
with tab2:
    st.header("🔍 DBSCAN Density-Based Clustering")

    if geo_metrics and "dbscan" in geo_metrics:
        col1, col2 = st.columns(2)
        with col1:
            score = geo_metrics["dbscan"]["silhouette"]
            st.metric("Silhouette Score", f"{score:.4f}" if score else "N/A")
        with col2:
            dbi = geo_metrics["dbscan"]["davies_bouldin"]
            st.metric("Davies-Bouldin Index", f"{dbi:.4f}" if dbi else "N/A")

        st.info("🔍 DBSCAN finds natural crime density clusters and filters outliers effectively.")

        if MAP_PATH.exists():
            st.subheader("🌆 Interactive DBSCAN Cluster Map")
            with open(MAP_PATH, "r", encoding="utf-8") as f:
                html = f.read()
            components.html(html, height=600, scrolling=False)
        else:
            st.warning("⚠️ DBSCAN map not found. Run `geo_clustering.py` again.")
    else:
        st.warning("⚠️ DBSCAN metrics missing. Please rerun `geo_clustering.py`.")

# ======================================================
# TAB 3: HIERARCHICAL
# ======================================================
with tab3:
    st.header("🌳 Hierarchical Clustering Relationships")

    if geo_metrics and "hierarchical" in geo_metrics:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Silhouette Score", f"{geo_metrics['hierarchical']['silhouette']:.4f}")
        with col2:
            st.metric("Davies-Bouldin Index", f"{geo_metrics['hierarchical']['davies_bouldin']:.4f}")

        if DENDRO_PATH.exists():
            st.subheader("📉 Dendrogram of Geographic Crime Zones")
            st.image(str(DENDRO_PATH), caption="Hierarchical clustering structure of crime zones")
        else:
            st.warning("⚠️ Dendrogram not found. Run `geo_clustering.py` to generate it.")
    else:
        st.warning("⚠️ Hierarchical metrics missing.")

# ======================================================
# TAB 4: PERFORMANCE COMPARISON
# ======================================================
with tab4:
    st.header("📊 Model Performance Comparison")

    comparison = []
    if geo_metrics:
        for algo, vals in geo_metrics.items():
            comparison.append({
                "Algorithm": f"Geo {algo.upper()}",
                "Silhouette": vals.get("silhouette", 0),
                "Davies-Bouldin": vals.get("davies_bouldin", 0)
            })
    if temp_metrics and "silhouette" in temp_metrics:
        comparison.append({
            "Algorithm": "Temporal KMeans",
            "Silhouette": temp_metrics["silhouette"],
            "Davies-Bouldin": temp_metrics["davies_bouldin"]
        })

    if comparison:
        df_comp = pd.DataFrame(comparison)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(
                df_comp,
                x="Algorithm",
                y="Silhouette",
                color="Silhouette",
                color_continuous_scale="Teal",
                title="Silhouette Score Comparison"
            )
            fig1.update_layout(height=400, font=dict(family="Poppins, sans-serif"))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.bar(
                df_comp,
                x="Algorithm",
                y="Davies-Bouldin",
                color="Davies-Bouldin",
                color_continuous_scale="Reds",
                title="Davies-Bouldin Index Comparison"
            )
            fig2.update_layout(height=400, font=dict(family="Poppins, sans-serif"))
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ No metrics found to compare.")

    st.markdown("""
    ---
    ### 📘 Understanding the Metrics
    - **Silhouette Score (−1 → +1):** Higher = better cluster separation  
    - **Davies-Bouldin Index (0 → ∞):** Lower = better cluster distinction  

    **Good clustering:**
    - Silhouette > 0.5 (Excellent)
    - DB Index < 1.0 (Strong separation)
    """)

# ======================================================
# SUMMARY
# ======================================================
st.markdown("---")
st.subheader("💡 Key Insights")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="insight-box">
        <strong>🌍 Geographic Insights</strong>
        <ul>
            <li>9 major hotspots identified via K-Means</li>
            <li>DBSCAN revealed natural dense crime clusters</li>
            <li>Hierarchical clustering mapped relational zone patterns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="insight-box">
        <strong>⏰ Temporal Insights</strong>
        <ul>
            <li>4 major time-based clusters identified</li>
            <li>Peak activity: <strong>5 PM–6 PM</strong> & summer months</li>
            <li>Seasonal patterns help forecast risk zones</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.success("✅ Clustering analysis visualization ready! Explore hotspots and temporal behavior interactively.")