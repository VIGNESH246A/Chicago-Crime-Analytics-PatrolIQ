"""
PatrolIQ - Geographic Clustering
---------------------------------------
Performs geographic clustering using KMeans, DBSCAN, and Hierarchical models.
Generates metrics, cluster center coordinates, and visual maps.
"""

import pandas as pd
import numpy as np
import joblib
import json
import folium
from folium.plugins import HeatMap
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import linkage, dendrogram
from pathlib import Path
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "model_ready_data.csv"
REPORTS_DIR = BASE_DIR / "reports" / "summaries"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
MODELS_DIR = BASE_DIR / "models" / "clustering"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# LOAD DATA
# ======================================================
print("📂 Loading data...")
df = pd.read_csv(DATA_PATH, low_memory=False)

# --- Detect coordinate columns automatically ---
possible_lat = [c for c in df.columns if "lat" in c.lower()]
possible_lon = [c for c in df.columns if "lon" in c.lower()]

if not possible_lat or not possible_lon:
    raise KeyError("❌ No coordinate columns found (latitude/longitude).")

lat_col = possible_lat[0]
lon_col = possible_lon[0]
coords = df[[lat_col, lon_col]].dropna()
coords = coords.sample(min(100000, len(coords)), random_state=42)

print(f"✅ Found coordinate columns: {lat_col}, {lon_col}")
print(f"✅ Data loaded: {coords.shape}")

# ======================================================
# GEO CLUSTERING
# ======================================================
metrics = {"kmeans": {}, "dbscan": {}, "hierarchical": {}}

# ---------- KMEANS ----------
print("🔹 Running KMeans (k=9)...")
kmeans = KMeans(n_clusters=9, random_state=42, n_init=10)
labels_km = kmeans.fit_predict(coords)
metrics["kmeans"]["silhouette"] = float(silhouette_score(coords, labels_km))
metrics["kmeans"]["davies_bouldin"] = float(davies_bouldin_score(coords, labels_km))
print(f"✅ KMeans trained | Silhouette: {metrics['kmeans']['silhouette']:.4f}")

# Save model
joblib.dump(kmeans, MODELS_DIR / "kmeans_geo_k9.pkl")

# Save cluster centers with standard column names
centers = pd.DataFrame(kmeans.cluster_centers_, columns=[lat_col, lon_col])
centers = centers.rename(columns={lat_col: "Latitude", lon_col: "Longitude"})
centers.to_csv(REPORTS_DIR / "kmeans_geo_centers_k9.csv", index=False)
print("✅ Saved KMeans centers → Latitude, Longitude columns standardized")

# ---------- DBSCAN ----------
print("🔹 Running DBSCAN...")
dbscan = DBSCAN(eps=0.005, min_samples=30, n_jobs=-1)
labels_db = dbscan.fit_predict(coords)

valid_mask = labels_db != -1
if valid_mask.sum() > 100:
    metrics["dbscan"]["silhouette"] = float(silhouette_score(coords[valid_mask], labels_db[valid_mask]))
    metrics["dbscan"]["davies_bouldin"] = float(davies_bouldin_score(coords[valid_mask], labels_db[valid_mask]))
else:
    metrics["dbscan"]["silhouette"] = None
    metrics["dbscan"]["davies_bouldin"] = None
print(f"✅ DBSCAN trained | Clusters found: {len(set(labels_db)) - 1}")

# ---------- Generate DBSCAN map ----------
try:
    print("🗺️ Generating DBSCAN map...")
    dbscan_coords = coords.copy()
    dbscan_coords["Cluster"] = labels_db

    center_lat = dbscan_coords[lat_col].mean()
    center_lon = dbscan_coords[lon_col].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    cluster_colors = plt.cm.tab10(np.linspace(0, 1, 10))

    for c in set(labels_db):
        if c == -1:
            continue
        cluster_points = dbscan_coords[dbscan_coords["Cluster"] == c]
        HeatMap(
            list(zip(cluster_points[lat_col], cluster_points[lon_col])),
            radius=6,
            blur=10,
            min_opacity=0.4
        ).add_to(m)

    output_map = FIGURES_DIR / "map_dbscan_geo.html"
    m.save(str(output_map))
    print(f"✅ DBSCAN map saved → {output_map}")
except Exception as e:
    print(f"⚠️ Map generation skipped due to: {e}")

# ---------- HIERARCHICAL ----------
print("🔹 Running Hierarchical Clustering (sample 10k for memory safety)...")
sampled = coords.sample(min(10000, len(coords)), random_state=42)
hier = AgglomerativeClustering(n_clusters=9, linkage="ward")
labels_h = hier.fit_predict(sampled)

metrics["hierarchical"]["silhouette"] = float(silhouette_score(sampled, labels_h))
metrics["hierarchical"]["davies_bouldin"] = float(davies_bouldin_score(sampled, labels_h))
print(f"✅ Hierarchical trained | Silhouette: {metrics['hierarchical']['silhouette']:.4f}")

# ---------- Dendrogram ----------
try:
    print("🌳 Generating dendrogram...")
    linkage_matrix = linkage(sampled.sample(2000, random_state=42), method='ward')
    plt.figure(figsize=(10, 6))
    dendrogram(linkage_matrix, truncate_mode="level", p=5)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample Index")
    plt.ylabel("Distance")
    dendro_path = FIGURES_DIR / "dendrogram_geo.png"
    plt.savefig(dendro_path, bbox_inches="tight")
    plt.close()
    print(f"✅ Dendrogram saved → {dendro_path}")
except Exception as e:
    print(f"⚠️ Dendrogram skipped due to: {e}")

# ======================================================
# SAVE METRICS
# ======================================================
out_path = REPORTS_DIR / "geo_clustering_metrics.json"
with open(out_path, "w") as f:
    json.dump(metrics, f, indent=4)

print("\n✅ Metrics saved →", out_path)
for k, v in metrics.items():
    print(f"📊 {k.upper()} - Silhouette: {v['silhouette']} | DB Index: {v['davies_bouldin']}")
print("\n🏁 Geographic clustering completed successfully.")
