"""
PatrolIQ - Temporal Crime Clustering
---------------------------------------
Clusters crime data based on temporal features:
Hour, Weekday, Month, Season, and Weekend/Weekday patterns.
Generates cluster metrics and summaries for PatrolIQ dashboards.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from pathlib import Path
import json
import joblib
import warnings
warnings.filterwarnings("ignore")

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "model_ready_data.csv"
REPORTS_DIR = BASE_DIR / "reports" / "summaries"
MODELS_DIR = BASE_DIR / "models" / "temporal"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# LOAD DATA
# ======================================================
print("📂 Loading model-ready data...")
df = pd.read_csv(DATA_PATH, low_memory=False)

# Select key temporal columns
temporal_cols = ["Year", "Month", "Weekday", "Hour", "IsWeekend", "SeasonLabel", "TimeLabel"]
df_temp = df[temporal_cols].copy()
print(f"✅ Data loaded for temporal clustering: {df_temp.shape}")

# ======================================================
# PREPROCESSING
# ======================================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_temp)
joblib.dump(scaler, MODELS_DIR / "temporal_scaler.pkl")

# ======================================================
# KMEANS CLUSTERING (multiple K)
# ======================================================
results = {}
for k in range(4, 9):
    print(f"🔹 Running KMeans (k={k})...")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    sil = float(silhouette_score(X_scaled, labels))
    db = float(davies_bouldin_score(X_scaled, labels))
    results[k] = {"silhouette": sil, "davies_bouldin": db}
    print(f"✅ K={k} | Silhouette={sil:.4f} | DB Index={db:.4f}")

# Choose best K based on silhouette
best_k = max(results, key=lambda x: results[x]["silhouette"])
print(f"\n🏆 Best number of clusters: K={best_k}")

# ======================================================
# FINAL MODEL TRAINING
# ======================================================
kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["TemporalCluster"] = kmeans_final.fit_predict(X_scaled)
joblib.dump(kmeans_final, MODELS_DIR / "kmeans_temporal.pkl")

# ======================================================
# CLUSTER SUMMARY
# ======================================================
cluster_summary = (
    df.groupby("TemporalCluster")[["Year", "Month", "Weekday", "Hour"]]
    .mean()
    .round(2)
)
cluster_summary["Count"] = df["TemporalCluster"].value_counts().sort_index().values

print("\n📊 Temporal Cluster Summary:\n", cluster_summary.head())

# ======================================================
# SAVE RESULTS
# ======================================================
metrics_path = REPORTS_DIR / "temporal_clustering_metrics.json"
summary_path = REPORTS_DIR / "temporal_cluster_summary.csv"

with open(metrics_path, "w") as f:
    json.dump(results, f, indent=4)

cluster_summary.to_csv(summary_path)

print("\n✅ Saved:")
print("📁", metrics_path)
print("📁", summary_path)
print("✅ Temporal clustering completed successfully!")
