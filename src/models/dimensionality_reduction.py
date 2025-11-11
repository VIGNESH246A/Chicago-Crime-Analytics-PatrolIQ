"""
dimensionality_reduction.py
------------------------------------
Performs dimensionality reduction (PCA + t-SNE)
for visualization and feature compression in PatrolIQ.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pathlib import Path
import time
import json
import warnings
warnings.filterwarnings("ignore")

# =====================================================
# Setup paths
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "model_ready_data.csv"
REPORT_DIR = BASE_DIR / "reports"
FIG_DIR = REPORT_DIR / "figures"
SUM_DIR = REPORT_DIR / "summaries"

FIG_DIR.mkdir(parents=True, exist_ok=True)
SUM_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Data
# =====================================================
print("📂 Loading model-ready data...")
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded data: {df.shape}")

# Select only numeric features
numeric_df = df.select_dtypes(include=[np.number])
print(f"✅ Numeric features selected: {numeric_df.shape[1]} columns")

# =====================================================
# PCA Reduction
# =====================================================
print("\n🔹 Running PCA reduction (2D)...")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_df)

pca = PCA(n_components=2, random_state=42)
pca_result = pca.fit_transform(X_scaled)

explained_var = pca.explained_variance_ratio_.sum()
print(f"✅ PCA completed | Total variance explained: {explained_var:.4f}")

# Save PCA results
df_pca = pd.DataFrame(pca_result, columns=["PCA1", "PCA2"])
df_pca.to_csv(SUM_DIR / "pca_reduced_data.csv", index=False)

# Plot PCA scatter
fig_pca = px.scatter(df_pca, x="PCA1", y="PCA2",
                     title=f"PCA Visualization (Variance Explained: {explained_var:.2%})",
                     opacity=0.6)
fig_pca.write_html(FIG_DIR / "pca_visualization.html")

# =====================================================
# t-SNE Reduction (fixed for sklearn>=1.7)
# =====================================================
print("\n🔹 Running t-SNE (2D)... (this may take a few minutes)")
start_time = time.time()

# Use a 10k sample for t-SNE due to compute cost
sample_df = numeric_df.sample(10000, random_state=42)
X_sample_scaled = scaler.transform(sample_df)

# ✅ Updated param: use max_iter instead of deprecated n_iter
tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
tsne_result = tsne.fit_transform(X_sample_scaled)

print(f"✅ t-SNE completed in {(time.time() - start_time):.2f} seconds")

df_tsne = pd.DataFrame(tsne_result, columns=["TSNE1", "TSNE2"])
df_tsne.to_csv(SUM_DIR / "tsne_reduced_data.csv", index=False)

# Interactive t-SNE scatter
fig_tsne = px.scatter(df_tsne, x="TSNE1", y="TSNE2",
                      title="t-SNE Crime Data Visualization (Sample 10k)",
                      opacity=0.6)
fig_tsne.write_html(FIG_DIR / "tsne_visualization.html")

# =====================================================
# Save Summary
# =====================================================
summary = {
    "pca_explained_variance": float(explained_var),
    "pca_components": pca.components_.tolist(),
    "tsne_sample_size": len(sample_df),
    "tsne_perplexity": 30,
    "tsne_iterations": 1000
}

with open(SUM_DIR / "dimensionality_reduction_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

print("\n✅ Dimensionality reduction completed successfully!")
print(f"📊 Reports saved to: {SUM_DIR}")
print(f"📈 Figures saved to: {FIG_DIR}")
