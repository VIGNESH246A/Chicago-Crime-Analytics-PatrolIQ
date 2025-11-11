"""
PatrolIQ - MLflow Model Monitoring & Performance Dashboard
----------------------------------------------------------
Track experiments, metrics, and model performance with stunning visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# =========================================================
# PATHS
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[3]
GEO_METRICS = BASE_DIR / "reports" / "summaries" / "geo_clustering_metrics.json"
TEMP_METRICS = BASE_DIR / "reports" / "summaries" / "temporal_clustering_metrics.json"
DIM_SUMMARY = BASE_DIR / "reports" / "summaries" / "dimensionality_reduction_summary.json"

# =========================================================
# PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="📈 MLflow Monitoring", 
    page_icon="📈", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS - STUNNING MODERN DESIGN
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Container */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1450px;
    }
    
    /* Animated gradient hero title */
    .hero-title {
        font-size: 4.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 12s ease infinite;
        margin-bottom: 0.4rem;
        letter-spacing: -3.5px;
        text-shadow: 0 0 50px rgba(102, 126, 234, 0.3);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 3rem;
        animation: fadeInUp 1.3s ease-out;
        letter-spacing: 0.3px;
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
    
    @keyframes slideInRight {
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
            transform: scale(0.85);
        }
        50% {
            transform: scale(1.02);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Advanced tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px;
        border-radius: 20px;
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
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
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
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid #667eea !important;
        color: white !important;
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Premium metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 2.2rem 1.8rem;
        border-radius: 24px;
        position: relative;
        transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        animation: scaleUp 0.7s ease-out;
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
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.08), transparent);
        transform: rotate(45deg);
        transition: all 0.7s ease;
    }
    
    div[data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-12px) scale(1.04);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.25);
        border-color: #667eea;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 3.2rem;
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
    
    /* Modern headers */
    h1 {
        color: #0f172a;
        font-weight: 800;
        margin-top: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.6rem;
        margin-top: 2.8rem;
        margin-bottom: 2rem;
        position: relative;
        padding-bottom: 1.2rem;
        animation: slideInRight 0.9s ease-out;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 120px;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 3px;
        animation: expandLine 1.2s ease-out;
    }
    
    @keyframes expandLine {
        from { width: 0; }
        to { width: 120px; }
    }
    
    h3 {
        color: #334155;
        font-weight: 700;
        font-size: 1.7rem;
        margin-top: 2rem;
    }
    
    /* Enhanced alert boxes */
    .stAlert {
        border-radius: 20px;
        border: none;
        padding: 1.4rem 1.8rem;
        animation: scaleUp 0.6s ease-out;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
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
        border-left: 6px solid #f59e0b;
    }
    
    [data-testid="stError"] {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        color: #991b1b;
        border-left: 6px solid #ef4444;
    }
    
    /* Plotly chart styling */
    .js-plotly-plot {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: scaleUp 0.8s ease-out;
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
    }
    
    /* Divider */
    hr {
        margin: 4rem 0;
        border: none;
        height: 4px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        border-radius: 2px;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #1e293b !important;
        border-radius: 16px;
        border: 2px solid #334155;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    code {
        font-family: 'JetBrains Mono', monospace;
        background: #f1f5f9;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        color: #667eea;
        font-weight: 600;
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
        border-radius: 16px;
        padding: 1rem 2.8rem;
        font-weight: 700;
        transition: all 0.35s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
        font-size: 1.05rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.45);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        margin: 0.3rem;
        animation: scaleUp 0.5s ease-out;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 2px solid #10b981;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        border: 2px solid #3b82f6;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        border: 2px solid #e2e8f0;
        font-weight: 700;
        color: #334155;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
    }
    
    /* Performance metric cards */
    .perf-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid #f1f5f9;
        transition: all 0.4s ease;
        animation: slideInRight 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .perf-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2);
    }
    
    .perf-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .perf-card strong {
        font-size: 1.3rem;
        color: #0f172a;
        display: block;
        margin-bottom: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown('<h1 class="hero-title">📈 MLflow Intelligence Center</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🔬 Advanced Model Performance Tracking & Experiment Analytics</p>', unsafe_allow_html=True)

# =========================================================
# LOAD METRICS
# =========================================================
@st.cache_data
def load_all_metrics():
    metrics = {}
    
    # Geographic metrics
    if GEO_METRICS.exists():
        try:
            with open(GEO_METRICS, 'r', encoding='utf-8') as f:
                metrics['geo'] = json.load(f)
        except Exception as e:
            st.error(f"❌ Error loading geographic metrics: {e}")
    
    # Temporal metrics
    if TEMP_METRICS.exists():
        try:
            with open(TEMP_METRICS, 'r', encoding='utf-8') as f:
                temp_raw = json.load(f)
                # Handle nested structure {4: {...}, 5: {...}} or direct {...}
                if temp_raw and isinstance(temp_raw, dict):
                    if all(isinstance(k, (int, str)) and str(k).isdigit() for k in temp_raw.keys()):
                        # Nested format - find best k
                        best_k = max(temp_raw, key=lambda k: temp_raw[k].get('silhouette', 0))
                        metrics['temp'] = {
                            'k': best_k,
                            'silhouette': temp_raw[best_k].get('silhouette'),
                            'davies_bouldin': temp_raw[best_k].get('davies_bouldin')
                        }
                    else:
                        # Direct format
                        metrics['temp'] = temp_raw
        except Exception as e:
            st.error(f"❌ Error loading temporal metrics: {e}")
    
    # Dimensionality reduction
    if DIM_SUMMARY.exists():
        try:
            with open(DIM_SUMMARY, 'r', encoding='utf-8') as f:
                metrics['dim'] = json.load(f)
        except Exception as e:
            st.error(f"❌ Error loading dimensionality metrics: {e}")
    
    return metrics

# =========================================================
# LOAD DATA
# =========================================================
with st.spinner("🔄 Loading experiment metrics..."):
    metrics = load_all_metrics()

if not metrics:
    st.error("❌ No metrics found. Please run the following scripts:")
    st.code("""
# Run these commands to generate metrics:
python src/models/geo_clustering.py
python src/models/temporal_clustering.py
python src/models/dimensionality_reduction.py
    """, language="bash")
    st.stop()

st.success(f"✅ Successfully loaded {len(metrics)} experiment type(s)")

# =========================================================
# OVERVIEW METRICS
# =========================================================
st.header("🎯 Experiment Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Experiment Types", len(metrics), help="Number of different experiment categories")

with col2:
    total_models = 0
    if 'geo' in metrics:
        total_models += len(metrics['geo'])
    if 'temp' in metrics:
        total_models += 1
    if 'dim' in metrics:
        total_models += 1
    st.metric("Total Models", total_models, help="Total trained models across all experiments")

with col3:
    status = "🟢 Active" if metrics else "🔴 Inactive"
    st.metric("MLflow Status", status, help="Current MLflow tracking status")

with col4:
    st.metric("Tracking Port", "5000", help="MLflow UI server port")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Model Performance",
    "🔬 Experiment Comparison",
    "📈 Metrics Dashboard",
    "🎯 Best Models",
    "🔗 MLflow UI"
])

# =========================================================
# TAB 1 - Model Performance
# =========================================================
with tab1:
    st.header("📊 Comprehensive Model Performance")
    
    # Geographic Clustering
    if 'geo' in metrics:
        st.subheader("🗺️ Geographic Clustering Models")
        
        geo_data = []
        for model_name, model_metrics in metrics['geo'].items():
            geo_data.append({
                "Model": model_name.upper(),
                "Silhouette Score": model_metrics.get("silhouette", 0),
                "Davies-Bouldin Index": model_metrics.get("davies_bouldin", 0)
            })
        
        if geo_data:
            geo_df = pd.DataFrame(geo_data)
            st.dataframe(
                geo_df.style.background_gradient(cmap='RdYlGn', subset=['Silhouette Score'])
                      .background_gradient(cmap='RdYlGn_r', subset=['Davies-Bouldin Index']),
                use_container_width=True
            )
            
            # Performance visualization
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(
                    geo_df,
                    x="Model",
                    y="Silhouette Score",
                    color="Silhouette Score",
                    color_continuous_scale=["#fca5a5", "#fbbf24", "#a7f3d0", "#10b981"],
                    title="Geographic Model Silhouette Scores"
                )
                fig1.update_layout(height=400, font=dict(family="Inter, sans-serif"))
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(
                    geo_df,
                    x="Model",
                    y="Davies-Bouldin Index",
                    color="Davies-Bouldin Index",
                    color_continuous_scale=["#10b981", "#a7f3d0", "#fbbf24", "#fca5a5"],
                    title="Geographic Model Davies-Bouldin Index"
                )
                fig2.update_layout(height=400, font=dict(family="Inter, sans-serif"))
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
    
    # Temporal Clustering
    if 'temp' in metrics:
        st.subheader("⏰ Temporal Clustering Model")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Optimal K", metrics['temp'].get('k', 'N/A'))
        with col2:
            st.metric("Silhouette Score", f"{metrics['temp'].get('silhouette', 0):.4f}")
        with col3:
            st.metric("Davies-Bouldin", f"{metrics['temp'].get('davies_bouldin', 0):.4f}")
        
        st.markdown("---")
    
    # Dimensionality Reduction
    if 'dim' in metrics:
        st.subheader("🔬 Dimensionality Reduction Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            if 'pca_explained_variance' in metrics['dim']:
                var = metrics['dim']['pca_explained_variance']
                st.metric("PCA Explained Variance", f"{var*100:.2f}%")
        
        with col2:
            if 'n_components' in metrics['dim']:
                st.metric("Optimal Components", metrics['dim']['n_components'])

# =========================================================
# TAB 2 - Experiment Comparison
# =========================================================
with tab2:
    st.header("🔬 Cross-Experiment Performance Comparison")
    
    # Collect all silhouette scores
    comparison_data = []
    
    if 'geo' in metrics:
        for model, vals in metrics['geo'].items():
            comparison_data.append({
                "Experiment": "Geographic",
                "Model": model.upper(),
                "Silhouette": vals.get("silhouette", 0),
                "Davies-Bouldin": vals.get("davies_bouldin", 0)
            })
    
    if 'temp' in metrics:
        comparison_data.append({
            "Experiment": "Temporal",
            "Model": f"K-Means (k={metrics['temp'].get('k', '?')})",
            "Silhouette": metrics['temp'].get("silhouette", 0),
            "Davies-Bouldin": metrics['temp'].get("davies_bouldin", 0)
        })
    
    if comparison_data:
        comp_df = pd.DataFrame(comparison_data)
        
        # Unified comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Silhouette Score',
            x=[f"{row['Experiment']}<br>{row['Model']}" for _, row in comp_df.iterrows()],
            y=comp_df['Silhouette'],
            marker_color='#667eea',
            text=comp_df['Silhouette'].round(4),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Unified Model Performance Comparison",
            yaxis_title="Silhouette Score",
            height=500,
            font=dict(family="Inter, sans-serif"),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Detailed Comparison Table")
        st.dataframe(comp_df, use_container_width=True)
    else:
        st.warning("⚠️ No comparison data available")

# =========================================================
# TAB 3 - Metrics Dashboard
# =========================================================
with tab3:
    st.header("📈 Advanced Metrics Dashboard")
    
    # Radar chart for geographic models
    if 'geo' in metrics:
        st.subheader("🎯 Geographic Models - Performance Radar")
        
        fig = go.Figure()
        
        for model, vals in metrics['geo'].items():
            # Normalize metrics for radar chart
            silhouette = vals.get('silhouette', 0)
            db_index = vals.get('davies_bouldin', 0)
            db_normalized = max(0, 1 - (db_index / 2))  # Normalize DB (lower is better)
            
            fig.add_trace(go.Scatterpolar(
                r=[silhouette, db_normalized, (silhouette + db_normalized) / 2],
                theta=['Silhouette', 'DB Index (norm)', 'Overall'],
                fill='toself',
                name=model.upper()
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            height=500,
            font=dict(family="Inter, sans-serif")
        )
        
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 4 - Best Models
# =========================================================
with tab4:
    st.header("🎯 Best Performing Models")
    
    # Find best geographic model
    if 'geo' in metrics:
        st.markdown('<div class="perf-card">', unsafe_allow_html=True)
        st.markdown('<strong>🏆 Best Geographic Model</strong>', unsafe_allow_html=True)
        
        best_geo = max(metrics['geo'].items(), key=lambda x: x[1].get('silhouette', 0))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model", best_geo[0].upper())
        with col2:
            st.metric("Silhouette", f"{best_geo[1].get('silhouette', 0):.4f}")
        with col3:
            st.metric("Davies-Bouldin", f"{best_geo[1].get('davies_bouldin', 0):.4f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Best temporal model
    if 'temp' in metrics:
        st.markdown('<div class="perf-card">', unsafe_allow_html=True)
        st.markdown('<strong>⏰ Best Temporal Model</strong>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Optimal K", metrics['temp'].get('k', 'N/A'))
        with col2:
            st.metric("Silhouette", f"{metrics['temp'].get('silhouette', 0):.4f}")
        with col3:
            st.metric("Davies-Bouldin", f"{metrics['temp'].get('davies_bouldin', 0):.4f}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TAB 5 - MLflow UI
# =========================================================
with tab5:
    st.header("🔗 MLflow Tracking UI Access")
    
    st.markdown("""
    <div class="perf-card">
        <strong>📊 Access MLflow Tracking Server</strong>
        <p style="font-size: 1.1rem; color: #475569; margin-top: 1rem;">
            MLflow provides a comprehensive UI for tracking experiments, comparing runs, and analyzing model performance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<span class="status-badge badge-info">🌐 Local Server</span>', unsafe_allow_html=True)
        st.code("http://127.0.0.1:5000", language="text")
        
        st.markdown("### 🚀 Quick Start")
        st.code("""# Start MLflow server
mlflow ui --host 127.0.0.1 --port 5000

# Access in browser
# Navigate to: http://127.0.0.1:5000""", language="bash")
    
    with col2:
        st.markdown('<span class="status-badge badge-success">✅ Features Available</span>', unsafe_allow_html=True)
        st.markdown("""
        - 📊 **Experiment Tracking**: View all runs and metrics
        - 🔍 **Model Comparison**: Compare multiple models side-by-side
        - 📈 **Metric Visualization**: Interactive charts and plots
        - 💾 **Artifact Storage**: Access saved models and outputs
        - 🏷️ **Version Control**: Track model versions and lineage
        """)
    
    st.markdown("---")
    
    # Instructions
    st.subheader("📚 Complete Setup Guide")
    
    with st.expander("🔧 Installation & Configuration"):
        st.markdown("""
        ### Step 1: Install MLflow
        ```bash
        pip install mlflow
        ```
        
        ### Step 2: Start Tracking Server
        ```bash
        # Basic start
        mlflow ui
        
        # Custom host and port
        mlflow ui --host 127.0.0.1 --port 5000
        
        # With backend store
        mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
        ```
        
        ### Step 3: Access UI
        Open your browser and navigate to: **http://127.0.0.1:5000**
        """)
    
    with st.expander("📖 Using MLflow with PatrolIQ"):
        st.markdown("""
        ### Tracking Experiments
        
        All PatrolIQ models automatically log to MLflow:
        
        ```python
        import mlflow
        
        # Geographic clustering logs
        mlflow.log_param("algorithm", "kmeans")
        mlflow.log_metric("silhouette_score", 0.7234)
        
        # Temporal clustering logs
        mlflow.log_param("k", 4)
        mlflow.log_metric("davies_bouldin", 0.5432)
        ```
        
        ### View Experiments
        1. Navigate to MLflow UI at http://127.0.0.1:5000
        2. Select experiment: **PatrolIQ-Geographic** or **PatrolIQ-Temporal**
        3. Compare runs by clicking "Compare" button
        4. View metrics charts in the "Chart" tab
        """)
    
    with st.expander("🎯 Best Practices"):
        st.markdown("""
        ### Experiment Organization
        - Use consistent naming: `patroliq-{model_type}-{date}`
        - Tag runs with metadata: `crime_type`, `city`, `date_range`
        - Log hyperparameters before training
        - Save model artifacts after training
        
        ### Performance Monitoring
        - Track silhouette score for cluster quality
        - Monitor Davies-Bouldin index for separation
        - Compare runs across different time periods
        - Export metrics for reporting
        
        ### Model Versioning
        - Register best models in Model Registry
        - Add version descriptions and tags
        - Track production vs staging models
        - Document model lineage
        """)
    
    # Status check
    st.markdown("---")
    st.subheader("🔍 System Status Check")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metrics_status = "✅ Active" if metrics else "❌ No Data"
        st.markdown(f'<span class="status-badge {"badge-success" if metrics else "badge-warning"}">{metrics_status}</span>', unsafe_allow_html=True)
        st.caption("Metrics Available")
    
    with col2:
        geo_status = "✅ Tracked" if 'geo' in metrics else "⚠️ Missing"
        st.markdown(f'<span class="status-badge {"badge-success" if "geo" in metrics else "badge-warning"}">{geo_status}</span>', unsafe_allow_html=True)
        st.caption("Geographic Models")
    
    with col3:
        temp_status = "✅ Tracked" if 'temp' in metrics else "⚠️ Missing"
        st.markdown(f'<span class="status-badge {"badge-success" if "temp" in metrics else "badge-warning"}">{temp_status}</span>', unsafe_allow_html=True)
        st.caption("Temporal Models")

# =========================================================
# DEBUG SECTION (Expandable)
# =========================================================
st.markdown("---")
with st.expander("🔍 Debug: View Raw Metric Data"):
    st.json(metrics)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; padding: 2rem 0;">
    <strong>PatrolIQ MLflow Intelligence Center</strong><br>
    Advanced Model Performance Tracking & Experiment Analytics<br>
    <span style="font-size: 0.9rem;">Powered by MLflow • Built with Streamlit</span>
</div>
""", unsafe_allow_html=True)

st.success("✅ MLflow monitoring dashboard ready! Track your experiments and optimize model performance.")