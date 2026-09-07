import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ============================================================
# 1. PATHS
# ============================================================

project_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project"

data_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segmentation_cleaned.csv"
)

output_folder = os.path.join(
    project_folder,
    "outputs"
)

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(data_file)


# ============================================================
# 3. FINAL CLUSTERING FEATURES
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

X = df[features].copy()


# ============================================================
# 4. STANDARDIZE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# 5. TRAIN FINAL K-MEANS MODEL
# ============================================================

K = 3

kmeans = KMeans(
    n_clusters=K,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X_scaled)


# ============================================================
# 6. MODEL SCORE
# ============================================================

silhouette = silhouette_score(
    X_scaled,
    df["Cluster"]
)

print("\n========== FINAL MODEL ==========")

print("Algorithm: K-Means")
print("Number of clusters:", K)
print("Number of customers:", len(df))
print("Number of features:", len(features))
print("Silhouette Score:", round(silhouette, 4))


# ============================================================
# 7. CLUSTER SIZES
# ============================================================

print("\n========== CLUSTER SIZES ==========")

cluster_sizes = df["Cluster"].value_counts().sort_index()

for cluster, size in cluster_sizes.items():

    percentage = size / len(df) * 100

    print(
        f"Cluster {cluster}: "
        f"{size} customers "
        f"({percentage:.2f}%)"
    )


# ============================================================
# 8. CLUSTER PROFILE
# ============================================================

print("\n========== CLUSTER PROFILE ==========")

profile = df.groupby("Cluster")[features].mean()

print(
    profile.round(2).to_string()
)


# ============================================================
# 9. PRODUCT SPENDING PROFILE
# ============================================================

print("\n========== PRODUCT SPENDING PROFILE ==========")

product_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

product_profile = df.groupby("Cluster")[product_columns].mean()

print(
    product_profile.round(2).to_string()
)


# ============================================================
# 10. CAMPAIGN RESPONSE PROFILE
# ============================================================

print("\n========== CAMPAIGN RESPONSE PROFILE ==========")

campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response"
]

campaign_profile = (
    df.groupby("Cluster")[campaign_columns].mean() * 100
)

print(
    campaign_profile.round(2).to_string()
)


# ============================================================
# 11. SAVE SEGMENTED DATASET
# ============================================================

segmented_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segments.csv"
)

df.to_csv(
    segmented_file,
    index=False
)

print("\nSegmented dataset saved to:")
print(segmented_file)


# ============================================================
# 12. VISUALIZE CLUSTER SIZES
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    cluster_sizes.index.astype(str),
    cluster_sizes.values
)

plt.title("Customer Distribution by Segment")
plt.xlabel("Cluster")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "cluster_distribution.png"
    ),
    dpi=300
)

plt.show()


print("\nFinal clustering completed successfully!")
