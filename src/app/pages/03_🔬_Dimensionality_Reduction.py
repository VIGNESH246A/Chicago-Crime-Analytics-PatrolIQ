"""
PatrolIQ - Dimensionality Reduction Visualizations
--------------------------------------------------
Visualizes PCA and t-SNE results from dimensionality_reduction.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
PCA_PATH = BASE_DIR / "reports" / "summaries" / "pca_reduced_data.csv"
TSNE_PATH = BASE_DIR / "reports" / "summaries" / "tsne_reduced_data.csv"
SUMMARY_PATH = BASE_DIR / "reports" / "summaries" / "dimensionality_reduction_summary.json"

st.set_page_config(page_title="Dimensionality Reduction", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")

# ======================================================
# CUSTOM CSS - STUNNING MODERN DESIGN
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
    
    /* Animated gradient hero title */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 8s ease infinite;
        margin-bottom: 0.3rem;
        letter-spacing: -4px;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.35rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 3rem;
        animation: fadeInUp 1.2s ease-out;
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
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
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
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Modern tab design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px;
        border-radius: 20px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
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
        background: linear-gradient(135deg, #667eea, #764ba2);
        transition: left 0.4s ease;
        z-index: -1;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid #667eea !important;
        color: white !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Glowing metric cards */
    div[data-testid="metric-container"] {
        background: white;
        padding: 2rem 1.8rem;
        border-radius: 24px;
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: popIn 0.7s ease-out;
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
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.15), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    div[data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.03);
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
    
    /* Section headers with modern styling */
    h1 {
        color: #1e293b;
        font-weight: 800;
        margin-top: 2rem;
    }
    
    h2 {
        color: #334155;
        font-weight: 800;
        font-size: 2.5rem;
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        padding-bottom: 1rem;
        animation: slideIn 0.9s ease-out;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100px;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 3px;
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 100px; }
    }
    
    h3 {
        color: #475569;
        font-weight: 700;
        font-size: 1.6rem;
        margin-top: 1.8rem;
    }
    
    /* Vibrant alert boxes */
    .stAlert {
        border-radius: 18px;
        border: none;
        padding: 1.4rem 1.7rem;
        animation: popIn 0.6s ease-out;
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
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border-left: 6px solid #f59e0b;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: popIn 0.8s ease-out;
        border: 1px solid #f1f5f9;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
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
    
    /* Comparison card styling */
    .comparison-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid #f1f5f9;
        transition: all 0.4s ease;
        animation: slideIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
        min-height: 280px;
    }
    
    .comparison-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2, #f093fb);
    }
    
    .comparison-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .comparison-card h3 {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
    }
    
    .comparison-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .comparison-card li {
        padding: 0.7rem 0;
        color: #475569;
        font-size: 1.05rem;
        position: relative;
        padding-left: 2rem;
        line-height: 1.6;
    }
    
    .comparison-card li::before {
        content: '●';
        position: absolute;
        left: 0;
        font-size: 1.4rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .comparison-card li.pro::before {
        content: '✓';
        color: #10b981;
    }
    
    .comparison-card li.con::before {
        content: '✗';
        color: #ef4444;
    }
    
    /* Feature highlight boxes */
    .feature-box {
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        padding: 1.8rem;
        border-radius: 18px;
        border-left: 5px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
        animation: slideIn 0.8s ease-out;
    }
    
    .feature-box strong {
        color: #764ba2;
        font-size: 1.15rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .feature-box p {
        color: #475569;
        margin: 0;
        line-height: 1.7;
    }
    
    /* Stats badge */
    .stats-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 0.5rem 0.5rem 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: popIn 0.5s ease-out;
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
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown('<h1 class="hero-title">🔬 Dimensionality Nexus</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🎯 Transform High-Dimensional Crime Data into Actionable 2D Insights</p>', unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_pca():
    if PCA_PATH.exists():
        return pd.read_csv(PCA_PATH)
    return None

@st.cache_data
def load_tsne():
    if TSNE_PATH.exists():
        return pd.read_csv(TSNE_PATH)
    return None

@st.cache_data
def load_summary():
    if SUMMARY_PATH.exists():
        with open(SUMMARY_PATH) as f:
            return json.load(f)
    return None

pca_df = load_pca()
tsne_df = load_tsne()
summary = load_summary()

# ======================================================
# SUMMARY METRICS
# ======================================================
if summary:
    st.markdown("## 📊 Reduction Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "PCA Explained Variance",
            f"{summary.get('pca_explained_variance', 0) * 100:.2f}%",
            help="Proportion of variance captured by first 2 principal components"
        )
    with col2:
        st.metric(
            "t-SNE Sample Size",
            f"{summary.get('tsne_sample_size', 0):,}",
            help="Number of records visualized in t-SNE plot"
        )
    with col3:
        variance = summary.get('pca_explained_variance', 0) * 100
        quality = "Excellent" if variance > 80 else "Good" if variance > 60 else "Moderate"
        st.metric(
            "Reduction Quality",
            quality,
            help="Overall quality of dimensionality reduction"
        )

    st.markdown(f"""
    <div class="feature-box">
        <strong>🎯 Analysis Summary</strong>
        <p>Successfully reduced multi-dimensional crime data to 2D representations. 
        PCA captures <strong>{variance:.1f}%</strong> of the total variance, 
        indicating {quality.lower()} information retention during compression.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Summary metrics not found. Please run `dimensionality_reduction.py` first.")

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 PCA Visualization",
    "🎨 t-SNE Visualization",
    "⚖️ Method Comparison",
    "📚 Technical Details"
])

# ======================================================
# TAB 1: PCA
# ======================================================
with tab1:
    st.header("📈 Principal Component Analysis (PCA)")

    if pca_df is not None:
        st.success(f"✅ Successfully loaded {len(pca_df):,} data points for PCA visualization")

        # Create enhanced PCA visualization
        fig = px.scatter(
            pca_df,
            x="PCA1",
            y="PCA2",
            title="PCA 2D Projection of Crime Patterns",
            labels={
                "PCA1": "Principal Component 1 (Spatial Variance)", 
                "PCA2": "Principal Component 2 (Temporal Variance)"
            },
            opacity=0.6,
            color_discrete_sequence=['#667eea']
        )
        
        fig.update_traces(
            marker=dict(size=5, line=dict(width=0.5, color='white')),
            selector=dict(mode='markers')
        )
        
        fig.update_layout(
            height=650,
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='rgba(248,250,252,0.5)',
            paper_bgcolor='white',
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # PCA insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
                <strong>🔍 What PCA Reveals</strong>
                <p>Each point represents a crime incident, positioned by its most significant 
                characteristics. Clustering indicates similar crime patterns, while spread 
                shows data diversity.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <strong>💡 Interpretation Guide</strong>
                <p>Dense regions = common crime patterns<br>
                Outliers = unusual incidents<br>
                Axes = combined features (location, time, type)</p>
            </div>
            """, unsafe_allow_html=True)

        # Technical details
        st.markdown("### 🔬 Technical Specifications")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<span class="stats-badge">Linear Transformation</span>', unsafe_allow_html=True)
        with col2:
            st.markdown('<span class="stats-badge">Preserves Variance</span>', unsafe_allow_html=True)
        with col3:
            st.markdown('<span class="stats-badge">Fast Computation</span>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ PCA data not found. Please run `dimensionality_reduction.py` to generate visualizations.")

# ======================================================
# TAB 2: t-SNE
# ======================================================
with tab2:
    st.header("🎨 t-Distributed Stochastic Neighbor Embedding")

    if tsne_df is not None:
        st.success(f"✅ Visualizing {len(tsne_df):,} sampled data points with t-SNE")

        # Create enhanced t-SNE visualization
        fig = px.scatter(
            tsne_df,
            x="TSNE1",
            y="TSNE2",
            title="t-SNE 2D Visualization: Discovering Crime Pattern Clusters",
            labels={
                "TSNE1": "t-SNE Dimension 1", 
                "TSNE2": "t-SNE Dimension 2"
            },
            opacity=0.7,
            color_discrete_sequence=['#764ba2']
        )
        
        fig.update_traces(
            marker=dict(size=6, line=dict(width=0.5, color='white')),
            selector=dict(mode='markers')
        )
        
        fig.update_layout(
            height=650,
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='rgba(248,250,252,0.5)',
            paper_bgcolor='white',
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # t-SNE insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
                <strong>🎯 Cluster Discovery</strong>
                <p>t-SNE excels at revealing natural groupings in complex data. 
                Distinct clusters indicate crime patterns with similar characteristics 
                across multiple dimensions.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <strong>⚡ Non-Linear Mapping</strong>
                <p>Unlike PCA, t-SNE captures non-linear relationships, making it ideal 
                for discovering hidden patterns that linear methods might miss.</p>
            </div>
            """, unsafe_allow_html=True)

        # Technical details
        st.markdown("### 🔬 Technical Specifications")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<span class="stats-badge">Non-Linear Transform</span>', unsafe_allow_html=True)
        with col2:
            st.markdown('<span class="stats-badge">Preserves Local Structure</span>', unsafe_allow_html=True)
        with col3:
            st.markdown('<span class="stats-badge">Cluster Optimization</span>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ t-SNE data not found. Please run `dimensionality_reduction.py` to generate visualizations.")

# ======================================================
# TAB 3: COMPARISON
# ======================================================
with tab3:
    st.header("⚖️ PCA vs t-SNE: Choosing the Right Tool")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="comparison-card">
            <h3>📈 PCA</h3>
            <ul>
                <li class="pro"><strong>Fast:</strong> Processes millions of records efficiently</li>
                <li class="pro"><strong>Interpretable:</strong> Components have mathematical meaning</li>
                <li class="pro"><strong>Deterministic:</strong> Same input = same output</li>
                <li class="pro"><strong>Variance:</strong> Quantifies information retention</li>
                <li class="con"><strong>Linear:</strong> Cannot capture complex non-linear patterns</li>
                <li class="con"><strong>Global:</strong> May miss local cluster structures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="comparison-card">
            <h3>🎨 t-SNE</h3>
            <ul>
                <li class="pro"><strong>Clusters:</strong> Excellent at revealing natural groupings</li>
                <li class="pro"><strong>Non-linear:</strong> Captures complex relationships</li>
                <li class="pro"><strong>Visual:</strong> Creates intuitive, interpretable plots</li>
                <li class="pro"><strong>Local:</strong> Preserves neighborhood structures</li>
                <li class="con"><strong>Slow:</strong> Requires sampling for large datasets</li>
                <li class="con"><strong>Stochastic:</strong> Results vary between runs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Use case recommendations
    st.markdown("## 🎯 When to Use Each Method")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <strong>Use PCA for:</strong>
            <p>
            • Initial data exploration<br>
            • Feature engineering<br>
            • Data compression<br>
            • Preprocessing before ML models<br>
            • Understanding overall data structure
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <strong>Use t-SNE for:</strong>
            <p>
            • Discovering hidden clusters<br>
            • Final visualization for reports<br>
            • Exploring complex patterns<br>
            • Validating clustering results<br>
            • Presenting insights to stakeholders
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **Best Practice:** Use PCA for initial exploration and feature reduction, then apply t-SNE on PCA-reduced data for detailed cluster visualization.")

# ======================================================
# TAB 4: TECHNICAL DETAILS
# ======================================================
with tab4:
    st.header("📚 Technical Documentation")

    st.markdown("### 🔬 Methodology Overview")
    
    st.markdown("""
    <div class="feature-box">
        <strong>Principal Component Analysis (PCA)</strong>
        <p>
        PCA is a linear dimensionality reduction technique that identifies directions (principal components) 
        of maximum variance in the data. It projects high-dimensional data onto a lower-dimensional space 
        while preserving as much variance as possible.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Mathematical Foundation:**
    - Computes covariance matrix of features
    - Performs eigendecomposition to find principal components
    - Projects data onto top k eigenvectors
    - Preserves global structure and variance
    """)

    st.markdown("""
    <div class="feature-box">
        <strong>t-Distributed Stochastic Neighbor Embedding (t-SNE)</strong>
        <p>
        t-SNE is a non-linear technique that converts high-dimensional Euclidean distances into 
        conditional probabilities representing similarities. It minimizes the divergence between 
        high- and low-dimensional probability distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Key Parameters:**
    - **Perplexity:** Controls neighborhood size (typically 5-50)
    - **Learning Rate:** Step size for optimization (typically 10-1000)
    - **Iterations:** Number of optimization steps (typically 1000-5000)
    - **Metric:** Distance measure (Euclidean by default)
    """)

    st.markdown("---")
    st.markdown("### 📊 Implementation Details")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **PCA Pipeline:**
        ```python
        1. Standardize features (mean=0, std=1)
        2. Compute covariance matrix
        3. Extract eigenvalues/eigenvectors
        4. Project data onto top 2 components
        5. Calculate explained variance
        ```
        """)
    
    with col2:
        st.markdown("""
        **t-SNE Pipeline:**
        ```python
        1. Sample data (if > 10k records)
        2. Standardize features
        3. Set perplexity=30, n_iter=1000
        4. Optimize low-dimensional embedding
        5. Generate 2D visualization
        ```
        """)

    st.markdown("---")
    st.markdown("### 🎯 Quality Metrics")

    if summary:
        variance = summary.get('pca_explained_variance', 0) * 100
        
        st.markdown(f"""
        <div class="feature-box">
            <strong>PCA Explained Variance: {variance:.2f}%</strong>
            <p>
            This metric indicates how much information from the original high-dimensional data 
            is preserved in the 2D representation. Higher values mean better information retention.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Variance interpretation
        if variance >= 80:
            quality_msg = "🟢 Excellent - The 2D projection captures most of the data variance"
        elif variance >= 60:
            quality_msg = "🟡 Good - Adequate variance retention for most analyses"
        elif variance >= 40:
            quality_msg = "🟠 Moderate - Some information loss, but patterns still visible"
        else:
            quality_msg = "🔴 Limited - Significant information loss in 2D projection"
        
        st.info(f"**Quality Assessment:** {quality_msg}")

    st.markdown("---")
    st.markdown("### ⚙️ Configuration Parameters")

    params_df = pd.DataFrame({
        "Parameter": [
            "PCA Components",
            "PCA Standardization",
            "t-SNE Perplexity",
            "t-SNE Learning Rate",
            "t-SNE Iterations",
            "Sample Size (t-SNE)"
        ],
        "Value": [
            "2",
            "StandardScaler",
            "30",
            "200",
            "1000",
            "10,000"
        ],
        "Purpose": [
            "Reduce to 2D for visualization",
            "Normalize feature scales",
            "Balance local vs global structure",
            "Optimization step size",
            "Convergence iterations",
            "Computational efficiency"
        ]
    })

    st.dataframe(params_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 📈 Performance Characteristics")

    perf_col1, perf_col2 = st.columns(2)

    with perf_col1:
        st.markdown("""
        **Computational Complexity:**
        
        | Method | Time Complexity | Space Complexity |
        |--------|----------------|------------------|
        | PCA    | O(n × d²)      | O(d²)           |
        | t-SNE  | O(n² × d)      | O(n²)           |
        
        *where n = samples, d = features*
        """)

    with perf_col2:
        st.markdown("""
        **Scalability:**
        
        - **PCA:** Handles millions of records efficiently
        - **t-SNE:** Requires sampling for n > 10,000
        - **Hybrid:** Use PCA first, then t-SNE on reduced data
        - **Parallel:** Both support multi-core processing
        """)

    st.markdown("---")
    st.markdown("### 🔍 Common Applications")

    app_col1, app_col2, app_col3 = st.columns(3)

    with app_col1:
        st.markdown("""
        **Crime Analysis:**
        - Pattern identification
        - Hotspot detection
        - Temporal clustering
        - Resource allocation
        """)

    with app_col2:
        st.markdown("""
        **Data Science:**
        - Feature engineering
        - Anomaly detection
        - Preprocessing for ML
        - Data visualization
        """)

    with app_col3:
        st.markdown("""
        **Business Intelligence:**
        - Customer segmentation
        - Market analysis
        - Trend discovery
        - Report generation
        """)

# ======================================================
# FOOTER INSIGHTS
# ======================================================
st.markdown("---")
st.markdown("## 💡 Key Takeaways")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown("""
    <div class="comparison-card">
        <h3>🎯 Insight #1</h3>
        <p>Dimensionality reduction transforms complex crime data into intuitive 2D visualizations, 
        revealing patterns invisible in high-dimensional space.</p>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown("""
    <div class="comparison-card">
        <h3>📊 Insight #2</h3>
        <p>PCA provides fast, interpretable results ideal for initial exploration, while 
        t-SNE excels at discovering natural clusters for detailed analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    st.markdown("""
    <div class="comparison-card">
        <h3>🚀 Insight #3</h3>
        <p>Combined use of both methods provides comprehensive understanding: PCA for structure, 
        t-SNE for clusters, enabling data-driven decision making.</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# RECOMMENDATIONS
# ======================================================
st.markdown("---")
st.markdown("## 🎓 Recommendations for PatrolIQ")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("""
    <div class="feature-box">
        <strong>🔬 For Analysts</strong>
        <p>
        1. Start with PCA to understand overall data structure<br>
        2. Identify outliers and data quality issues<br>
        3. Use explained variance to assess reduction quality<br>
        4. Apply t-SNE for detailed cluster investigation<br>
        5. Cross-reference with geographic clustering results
        </p>
    </div>
    """, unsafe_allow_html=True)

with rec_col2:
    st.markdown("""
    <div class="feature-box">
        <strong>👮 For Law Enforcement</strong>
        <p>
        1. Use visualizations to identify crime pattern types<br>
        2. Correlate clusters with known hotspots<br>
        3. Integrate temporal patterns for resource planning<br>
        4. Monitor cluster changes over time<br>
        5. Share insights with command staff using visuals
        </p>
    </div>
    """, unsafe_allow_html=True)

st.success("✅ Dimensionality Reduction Dashboard Ready! Explore high-dimensional crime patterns in intuitive 2D space.")

# ======================================================
# ADDITIONAL RESOURCES
# ======================================================
with st.expander("📚 Additional Resources & References"):
    st.markdown("""
    ### Learn More About Dimensionality Reduction
    
    **Academic Papers:**
    - Van der Maaten & Hinton (2008): "Visualizing Data using t-SNE"
    - Jolliffe (2002): "Principal Component Analysis"
    - Wattenberg et al. (2016): "How to Use t-SNE Effectively"
    
    **Practical Guides:**
    - Scikit-learn documentation on PCA and t-SNE
    - Distill.pub interactive t-SNE tutorial
    - Towards Data Science dimensionality reduction guide
    
    **Best Practices:**
    - Always standardize data before dimensionality reduction
    - Use PCA as preprocessing for t-SNE on large datasets
    - Experiment with t-SNE perplexity for different insights
    - Validate results with domain knowledge
    - Combine with clustering algorithms for comprehensive analysis
    
    **PatrolIQ Integration:**
    - Results feed into clustering algorithms (K-Means, DBSCAN)
    - Supports temporal and geographic pattern discovery
    - Enables interactive exploration of crime data
    - Facilitates communication of complex patterns
    """)

with st.expander("⚙️ Configuration & Tuning Guide"):
    st.markdown("""
    ### PCA Configuration
    
    **Number of Components:**
    - Start with 2-3 for visualization
    - Increase to 10-50 for feature engineering
    - Use scree plot to identify elbow point
    
    **Standardization:**
    - Always use StandardScaler for mixed-scale features
    - Consider RobustScaler for outlier-heavy data
    - Use MinMaxScaler for bounded features only
    
    ### t-SNE Configuration
    
    **Perplexity (5-50):**
    - Lower (5-15): Emphasizes local structure, smaller clusters
    - Medium (20-30): Balanced view (default)
    - Higher (40-50): Emphasizes global structure, larger clusters
    
    **Learning Rate (10-1000):**
    - Too low: Slow convergence, stuck in local minima
    - Too high: Unstable optimization, poor results
    - Sweet spot: 100-500 for most datasets
    
    **Iterations:**
    - Minimum: 1000 for convergence
    - Recommended: 2000-5000 for quality results
    - Monitor convergence with KL divergence
    
    **Early Exaggeration:**
    - Controls initial cluster spacing
    - Default: 12.0 works well for most cases
    - Increase for more separated clusters
    """)

with st.expander("🐛 Troubleshooting Common Issues"):
    st.markdown("""
    ### PCA Issues
    
    **Problem:** Low explained variance (<40%)
    - **Cause:** Data may not have linear structure
    - **Solution:** Try non-linear methods (t-SNE, UMAP, kernel PCA)
    
    **Problem:** All points clustered together
    - **Cause:** Features not standardized
    - **Solution:** Apply StandardScaler before PCA
    
    ### t-SNE Issues
    
    **Problem:** "Crowding problem" - overlapping clusters
    - **Cause:** Perplexity too low or data truly overlapping
    - **Solution:** Increase perplexity or accept natural overlap
    
    **Problem:** Results change dramatically between runs
    - **Cause:** Stochastic optimization with different random seeds
    - **Solution:** Set random_state parameter for reproducibility
    
    **Problem:** Very slow computation
    - **Cause:** Large dataset (>10k samples)
    - **Solution:** Apply PCA first (50 components), then t-SNE
    
    **Problem:** All points in uniform blob
    - **Cause:** Too few iterations or inappropriate learning rate
    - **Solution:** Increase iterations to 2000-5000, adjust learning_rate
    
    ### General Issues
    
    **Problem:** Outliers dominating visualization
    - **Solution:** Filter outliers or use RobustScaler
    
    **Problem:** Categorical features causing issues
    - **Solution:** One-hot encode before reduction
    
    **Problem:** Missing values
    - **Solution:** Impute before dimensionality reduction
    """)