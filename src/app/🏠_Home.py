"""
PatrolIQ - Crime Analysis Dashboard
Main Streamlit Application Entry Point
Advanced Crime Intelligence Platform with Modern UI
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="PatrolIQ - Crime Analysis Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS - PREMIUM MODERN DESIGN
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Container */
    .main .block-container {
        padding: 1.5rem 2.5rem;
        max-width: 1500px;
    }
    
    /* Hero Section - Massive Animated Title */
    .hero-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 5.5rem;
        font-weight: 900;
        font-family: 'Clash Display', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: heroGradient 15s ease infinite;
        margin-bottom: 0.5rem;
        letter-spacing: -5px;
        line-height: 1.1;
        text-shadow: 0 0 80px rgba(102, 126, 234, 0.4);
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.8rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: float 3s ease-in-out infinite;
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 2rem;
        animation: fadeInUp 1.5s ease-out;
        letter-spacing: 0.3px;
        line-height: 1.6;
    }
    
    /* Animations */
    @keyframes heroGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
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
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleIn {
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
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        }
        50% {
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
        }
    }
    
    /* Premium Metric Cards */
    .metric-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 28px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 2px solid #f1f5f9;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: scaleIn 0.8s ease-out;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s ease;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-card:hover {
        transform: translateY(-15px) scale(1.03);
        border-color: #667eea;
        box-shadow: 0 30px 70px rgba(102, 126, 234, 0.25);
    }
    
    .metric-number {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Clash Display', sans-serif;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 1.05rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 24px;
        border: 2px solid #f1f5f9;
        transition: all 0.4s ease;
        animation: slideInLeft 0.8s ease-out;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.05), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: #667eea;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
        font-family: 'Clash Display', sans-serif;
    }
    
    .feature-description {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 500;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin-top: 1rem;
    }
    
    .feature-list li {
        padding: 0.6rem 0;
        color: #475569;
        font-size: 0.95rem;
        position: relative;
        padding-left: 2rem;
        line-height: 1.5;
    }
    
    .feature-list li::before {
        content: '✦';
        position: absolute;
        left: 0;
        color: #667eea;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 2.5rem;
        border-radius: 24px;
        border-left: 6px solid #667eea;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        animation: scaleIn 0.7s ease-out;
    }
    
    .info-box h3 {
        color: #1e293b;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-family: 'Clash Display', sans-serif;
    }
    
    .info-box p {
        color: #475569;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    /* Section Headers */
    h1, h2 {
        font-family: 'Clash Display', sans-serif;
        font-weight: 800;
    }
    
    h2 {
        color: #1e293b;
        font-size: 2.5rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        position: relative;
        padding-bottom: 1rem;
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
    }
    
    h3 {
        color: #334155;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    /* Quick Start Guide */
    .quick-start {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #f1f5f9;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    .quick-start-item {
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 16px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #334155;
    }
    
    .quick-start-item:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
    }
    
    .quick-start-number {
        display: inline-block;
        width: 35px;
        height: 35px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 35px;
        font-weight: 700;
        margin-right: 1rem;
        font-size: 1rem;
    }
    
    /* Alert/Info Styling */
    .stAlert {
        border-radius: 18px;
        border: none;
        padding: 1.3rem 1.6rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
        font-weight: 500;
        animation: scaleIn 0.6s ease-out;
    }
    
    [data-testid="stInfo"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        border-left: 6px solid #3b82f6;
    }
    
    /* Divider */
    hr {
        margin: 3rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        border-radius: 2px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 2.5rem 0;
        margin-top: 3rem;
        border-top: 2px solid #f1f5f9;
        font-weight: 500;
    }
    
    .footer-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 0.5rem;
    }
    
    /* Custom Scrollbar */
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
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MAIN PAGE
# =========================================================
def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🚔 ADVANCED CRIME INTELLIGENCE</div>
        <h1 class="hero-title">PatrolIQ</h1>
        <p class="hero-subtitle">
            Revolutionizing Public Safety with AI-Powered Crime Pattern Analysis<br>
            🎯 Real-Time Insights • 🗺️ Geographic Hotspots • ⏰ Temporal Predictions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Info Box
    st.markdown("""
    <div class="info-box">
        <h3>🌟 Welcome to the Future of Crime Analysis</h3>
        <p>PatrolIQ is a cutting-edge crime intelligence platform that leverages advanced machine learning 
        algorithms to identify patterns, predict hotspots, and provide actionable insights for law enforcement 
        and public safety officials. Explore comprehensive analytics through our interactive dashboard modules.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview Metrics
    st.markdown("<h2>📊 Platform Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">500K</div>
            <div class="metric-label">Crime Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">33</div>
            <div class="metric-label">Crime Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">9</div>
            <div class="metric-label">Hotspot Zones</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">4</div>
            <div class="metric-label">Time Patterns</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("<h2>🚀 Core Features & Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🗺️</span>
            <div class="feature-title">Geographic Intelligence</div>
            <div class="feature-description">
                Advanced spatial analysis to identify high-risk areas and crime concentration zones
            </div>
            <ul class="feature-list">
                <li>Interactive crime heatmaps with real-time filtering</li>
                <li>K-Means clustering identifies 9 major hotspots</li>
                <li>DBSCAN density-based anomaly detection</li>
                <li>Hierarchical clustering for zone relationships</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⏰</span>
            <div class="feature-title">Temporal Pattern Analysis</div>
            <div class="feature-description">
                Discover when crimes occur most frequently across different time scales
            </div>
            <ul class="feature-list">
                <li>Hourly, daily, and seasonal trend visualization</li>
                <li>Peak crime time identification algorithms</li>
                <li>Weekday vs weekend comparative analysis</li>
                <li>Multi-year trend tracking and forecasting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔬</span>
            <div class="feature-title">Advanced Analytics Suite</div>
            <div class="feature-description">
                Cutting-edge machine learning techniques for pattern discovery
            </div>
            <ul class="feature-list">
                <li>PCA & t-SNE visualizations for hidden patterns</li>
                <li>UMAP embeddings for cluster analysis</li>
                <li>Feature importance ranking and correlation</li>
                <li>Dimensionality reduction for insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📈</span>
            <div class="feature-title">Model Performance Tracking</div>
            <div class="feature-description">
                Comprehensive monitoring and optimization of ML models
            </div>
            <ul class="feature-list">
                <li>MLflow experiment tracking integration</li>
                <li>Real-time model performance metrics</li>
                <li>Silhouette & Davies-Bouldin scoring</li>
                <li>Automated cluster quality assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Start Guide
    st.markdown("<h2>🎯 Quick Navigation Guide</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="quick-start">
        <div class="quick-start-item">
            <span class="quick-start-number">1</span>
            <strong>Geographic Heatmaps</strong> → Explore crime density and distribution across Chicago
        </div>
        <div class="quick-start-item">
            <span class="quick-start-number">2</span>
            <strong>Temporal Analysis</strong> → Understand temporal patterns and peak crime periods
        </div>
        <div class="quick-start-item">
            <span class="quick-start-number">3</span>
            <strong>Clustering Results</strong> → View geographic and temporal crime pattern clusters
        </div>
        <div class="quick-start-item">
            <span class="quick-start-number">4</span>
            <strong>Dimensionality Reduction</strong> → Discover hidden relationships in crime data
        </div>
        <div class="quick-start-item">
            <span class="quick-start-number">5</span>
            <strong>MLflow Monitoring</strong> → Track and optimize model performance metrics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Pro Tip**: Use the sidebar navigation to seamlessly switch between analysis modules. All visualizations are fully interactive—hover, zoom, and filter to explore insights!")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-title">PatrolIQ Crime Intelligence Platform</div>
        <div>Powered by Streamlit • Scikit-learn • MLflow • Plotly</div>
        <div>Chicago Crime Data (2010-2025) • Built with ❤️ for Public Safety</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()