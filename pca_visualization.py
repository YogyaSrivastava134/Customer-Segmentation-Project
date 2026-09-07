import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# ============================================================
# 1. PATHS
# ============================================================

project_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project"

data_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segments.csv"
)

output_folder = os.path.join(
    project_folder,
    "outputs"
)

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# 2. LOAD SEGMENTED DATA
# ============================================================

df = pd.read_csv(data_file)


# ============================================================
# 3. CLUSTERING FEATURES
# ============================================================

features = [
    "Age",
    "Income",
    "Recency",
    "TotalSpending",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
    "TotalChildren"
]

X = df[features]


# ============================================================
# 4. STANDARDIZE
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# 5. PCA
# ============================================================

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

df["PCA1"] = X_pca[:, 0]
df["PCA2"] = X_pca[:, 1]


# ============================================================
# 6. EXPLAINED VARIANCE
# ============================================================

explained_variance = pca.explained_variance_ratio_

print("\n========== PCA RESULTS ==========")

print(
    f"PC1 explained variance: "
    f"{explained_variance[0] * 100:.2f}%"
)

print(
    f"PC2 explained variance: "
    f"{explained_variance[1] * 100:.2f}%"
)

print(
    f"Total explained variance: "
    f"{explained_variance.sum() * 100:.2f}%"
)


# ============================================================
# 7. VISUALIZE CLUSTERS
# ============================================================

plt.figure(figsize=(9, 6))

for cluster in sorted(df["Cluster"].unique()):

    cluster_data = df[df["Cluster"] == cluster]

    plt.scatter(
        cluster_data["PCA1"],
        cluster_data["PCA2"],
        label=f"Cluster {cluster}",
        alpha=0.6
    )


plt.title("Customer Segments Visualized Using PCA")

plt.xlabel(
    f"Principal Component 1 "
    f"({explained_variance[0] * 100:.1f}% variance)"
)

plt.ylabel(
    f"Principal Component 2 "
    f"({explained_variance[1] * 100:.1f}% variance)"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "customer_segments_pca.png"
    ),
    dpi=300
)

plt.show()


print("\nPCA visualization saved to:")
print(
    os.path.join(
        output_folder,
        "customer_segments_pca.png"
    )
)
