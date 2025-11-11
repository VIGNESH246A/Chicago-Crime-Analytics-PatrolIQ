"""
PatrolIQ - Temporal Crime Pattern Analysis
------------------------------------------
Interactive temporal trend visualization and clustering insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# ======================================================
# PATHS
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH_01 = BASE_DIR / "data" / "processed" / "sample_250000_rows_01.csv"
DATA_PATH_02 = BASE_DIR / "data" / "processed" / "sample_250000_rows_02.csv"
TEMP_METRICS = BASE_DIR / "reports" / "summaries" / "temporal_clustering_metrics.json"
TEMP_SUMMARY = BASE_DIR / "reports" / "summaries" / "temporal_cluster_summary.csv"

st.set_page_config(page_title="Temporal Analysis", page_icon="⏰", layout="wide", initial_sidebar_state="collapsed")

# ======================================================
# CUSTOM CSS - STUNNING MODERN DESIGN
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;700;800&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Container */
    .main .block-container {
        padding: 1.5rem 2.5rem;
        max-width: 1450px;
    }
    
    /* Animated gradient hero title */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #FF6B9D, #C06C84, #6C5B7B, #355C7D);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientWave 10s ease infinite;
        margin-bottom: 0.3rem;
        letter-spacing: -4px;
        text-shadow: 0 0 40px rgba(255, 107, 157, 0.3);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.35rem;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 2.5rem;
        animation: fadeInUp 1.2s ease-out;
        letter-spacing: 0.5px;
    }
    
    /* Gradient animation */
    @keyframes gradientWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideRight {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes popIn {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Futuristic tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        padding: 10px;
        border-radius: 20px;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 58px;
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 14px;
        padding: 0 30px;
        font-weight: 700;
        font-size: 14.5px;
        color: #6b7280;
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
        background: linear-gradient(120deg, #FF6B9D, #C06C84);
        transition: left 0.35s ease;
        z-index: -1;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FF6B9D;
        color: #FF6B9D;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 107, 157, 0.25);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #FF6B9D 0%, #C06C84 100%) !important;
        border: 2px solid #FF6B9D !important;
        color: white !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.35);
    }
    
    /* Glowing metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 22px;
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: popIn 0.7s ease-out;
        border: 2px solid #f3f4f6;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 107, 157, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    div[data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 50px rgba(255, 107, 157, 0.2);
        border-color: #FF6B9D;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 50%, #6C5B7B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 700;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Section headers with underline effect */
    h1 {
        color: #1f2937;
        font-weight: 800;
        margin-top: 2rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    h2 {
        color: #374151;
        font-weight: 800;
        font-size: 2.5rem;
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        padding-bottom: 1rem;
        animation: slideRight 0.9s ease-out;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100px;
        height: 5px;
        background: linear-gradient(90deg, #FF6B9D, #C06C84);
        border-radius: 3px;
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 100px; }
    }
    
    h3 {
        color: #4b5563;
        font-weight: 700;
        font-size: 1.6rem;
        margin-top: 1.8rem;
    }
    
    /* Vibrant alert boxes */
    .stAlert {
        border-radius: 18px;
        border: none;
        padding: 1.3rem 1.6rem;
        animation: popIn 0.6s ease-out;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
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
        border-radius: 22px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: popIn 0.8s ease-out;
        border: 1px solid #f3f4f6;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 50px rgba(255, 107, 157, 0.15);
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid #f3f4f6;
    }
    
    /* Divider */
    hr {
        margin: 3.5rem 0;
        border: none;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FF6B9D, #C06C84, transparent);
        border-radius: 2px;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #FF6B9D;
        box-shadow: 0 4px 12px rgba(255, 107, 157, 0.15);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f9fafb;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF6B9D, #C06C84);
        border-radius: 10px;
        border: 3px solid #f9fafb;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #C06C84, #FF6B9D);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.9rem 2.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
        background: linear-gradient(135deg, #C06C84 0%, #FF6B9D 100%);
    }
    
    /* Metric highlight boxes */
    .metric-highlight {
        background: linear-gradient(135deg, #fff5f7 0%, #ffe4e9 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 5px solid #FF6B9D;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.1);
        animation: slideRight 0.8s ease-out;
    }
    
    .metric-highlight strong {
        color: #C06C84;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="hero-title">⏰ Temporal Intelligence Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🕐 Discover Hourly, Daily, Monthly & Seasonal Crime Patterns with AI-Powered Clustering</p>', unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data():
    df_01 = pd.read_csv(DATA_PATH_01, low_memory=False)
    df_02 = pd.read_csv(DATA_PATH_02, low_memory=False)
    df = pd.concat([df_01, df_02], ignore_index=True)
    df["Date"] = pd.to_datetime(df.get("Date"), errors="coerce")
    df = df.dropna(subset=["Date"])

    if "Year" not in df.columns:
        df["Year"] = df["Date"].dt.year
    if "Month" not in df.columns:
        df["Month"] = df["Date"].dt.month
    if "Day" not in df.columns:
        df["Day"] = df["Date"].dt.day
    if "Hour" not in df.columns:
        df["Hour"] = df["Date"].dt.hour
    if "Weekday" not in df.columns:
        df["Weekday"] = df["Date"].dt.weekday

    df["Season"] = df["Month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall"
    })

    return df


@st.cache_data
def load_metrics():
    if TEMP_METRICS.exists():
        with open(TEMP_METRICS, "r") as f:
            return json.load(f)
    return {}


@st.cache_data
def load_summary():
    if TEMP_SUMMARY.exists():
        return pd.read_csv(TEMP_SUMMARY)
    return None


df = load_data()
metrics = load_metrics()
summary = load_summary()

# ======================================================
# FIX STRUCTURE FROM YOUR TRAINING FILE
# ======================================================
# metrics = {4: {"silhouette": .., "davies_bouldin": ..}, ...}
if isinstance(metrics, dict) and not "silhouette" in metrics:
    best_k = max(metrics, key=lambda k: metrics[k]["silhouette"])
    best_metrics = metrics[best_k]
    metrics = {
        "k": best_k,
        "silhouette": best_metrics["silhouette"],
        "davies_bouldin": best_metrics["davies_bouldin"]
    }

# ======================================================
# UI LAYOUT
# ======================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Temporal Clustering",
    "📅 Hourly Patterns",
    "📆 Daily & Weekly Trends",
    "📊 Monthly & Seasonal Trends",
    "🔥 Heatmaps"
])

# ---------------- TAB 1 ----------------
with tab1:
    st.header("🎯 Temporal Crime Pattern Clustering")

    if metrics:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Number of Patterns", metrics.get("k", "N/A"))
        with col2:
            st.metric("Silhouette Score", f"{metrics.get('silhouette', 0):.4f}")
        with col3:
            st.metric("Davies-Bouldin Index", f"{metrics.get('davies_bouldin', 0):.4f}")

        if summary is not None:
            st.subheader("📊 Temporal Cluster Characteristics")
            st.dataframe(summary, use_container_width=True)

            # Polar plot visualization
            fig = go.Figure()
            colors = ['#FF6B9D', '#C06C84', '#6C5B7B', '#355C7D']
            for i, row in summary.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[row["Hour"], row["Weekday"], row["Month"]],
                    theta=["Hour", "Weekday", "Month"],
                    fill="toself",
                    name=f"Cluster {i}",
                    line=dict(color=colors[i % len(colors)], width=3)
                ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 24])),
                showlegend=True,
                height=500,
                title="Temporal Cluster Profiles",
                font=dict(family="Outfit, sans-serif")
            )
            st.plotly_chart(fig, use_container_width=True)

        st.info("💡 KMeans identified major time-based crime patterns like morning, afternoon, and night clusters.")
    else:
        st.warning("⚠️ Temporal clustering metrics not found. Run `temporal_clustering.py` first.")

# ---------------- TAB 2 ----------------
with tab2:
    st.header("📅 Hourly Patterns")

    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Select Years", years, default=years[-3:])
    filtered_df = df[df["Year"].isin(selected_years)]

    hourly = filtered_df["Hour"].value_counts().sort_index()
    fig = px.line(
        x=hourly.index, 
        y=hourly.values, 
        markers=True, 
        title="Crime Frequency by Hour"
    )
    fig.update_traces(line_color='#FF6B9D', marker=dict(size=10, color='#C06C84'))
    fig.update_layout(
        height=400, 
        xaxis_title="Hour of Day", 
        yaxis_title="Crimes",
        font=dict(family="Outfit, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

    top_hours = hourly.nlargest(3)
    col1, col2, col3 = st.columns(3)
    for i, (hour, count) in enumerate(top_hours.items()):
        with [col1, col2, col3][i]:
            st.metric(f"Peak Hour #{i+1}", f"{hour}:00", f"{count:,} crimes")

# ---------------- TAB 3 ----------------
with tab3:
    st.header("📆 Daily & Weekly Trends")

    weekday_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    weekday_counts = df["Weekday"].map(weekday_map).value_counts()
    weekday_counts = weekday_counts.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

    fig = px.bar(
        x=weekday_counts.index,
        y=weekday_counts.values,
        color=weekday_counts.values,
        color_continuous_scale=["#FFE4E9", "#FF6B9D", "#C06C84"],
        title="Crimes by Day of Week"
    )
    fig.update_layout(
        height=400, 
        xaxis_title="Day", 
        yaxis_title="Crimes",
        font=dict(family="Outfit, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.header("📊 Monthly & Seasonal Trends")

    monthly = df.groupby(["Year", "Month"]).size().reset_index(name="Count")
    monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(DAY=1))
    fig = px.line(monthly, x="Date", y="Count", markers=True, title="Monthly Crime Trend")
    fig.update_traces(line_color='#6C5B7B', marker=dict(size=8, color='#C06C84'))
    fig.update_layout(font=dict(family="Outfit, sans-serif"))
    st.plotly_chart(fig, use_container_width=True)

    season_counts = df["Season"].value_counts().reindex(["Winter", "Spring", "Summer", "Fall"])
    fig = px.bar(
        x=season_counts.index,
        y=season_counts.values,
        color=season_counts.values,
        color_continuous_scale=["#355C7D", "#6C5B7B", "#C06C84", "#FF6B9D"],
        title="Crimes by Season"
    )
    fig.update_layout(font=dict(family="Outfit, sans-serif"))
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 5 ----------------
with tab5:
    st.header("🔥 Temporal Heatmaps")

    weekday_map_full = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
                        4: "Friday", 5: "Saturday", 6: "Sunday"}
    heat_data = df.groupby(["Weekday", "Hour"]).size().reset_index(name="Count")
    pivot = heat_data.pivot(index="Weekday", columns="Hour", values="Count").fillna(0)
    pivot.index = pivot.index.map(weekday_map_full)

    fig = px.imshow(
        pivot,
        labels=dict(x="Hour", y="Day of Week", color="Crimes"),
        title="Crime Heatmap: Day vs Hour",
        color_continuous_scale=["#fff5f7", "#FFE4E9", "#FF6B9D", "#C06C84", "#6C5B7B"]
    )
    fig.update_layout(font=dict(family="Outfit, sans-serif"))
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ Temporal crime pattern dashboard ready!")