import pandas as pd
import numpy as np
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


# ============================================================
# 2. LOAD DATA
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

X = df[features].copy()


# ============================================================
# 4. STANDARDIZE
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# 5. EVALUATE K = 2, 3, 4, 5
# ============================================================

for k in [2, 3, 4, 5]:

    print("\n")
    print("=" * 60)
    print(f"CLUSTER ANALYSIS FOR K = {k}")
    print("=" * 60)

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    df["Cluster"] = kmeans.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        df["Cluster"]
    )

    print(f"\nSilhouette Score: {score:.4f}")

    print("\n========== CLUSTER SIZES ==========")

    cluster_sizes = df["Cluster"].value_counts().sort_index()

    for cluster, size in cluster_sizes.items():

        percentage = (size / len(df)) * 100

        print(
            f"Cluster {cluster}: "
            f"{size} customers "
            f"({percentage:.2f}%)"
        )


    print("\n========== CLUSTER PROFILES ==========")

    profile_columns = [
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

    profile = df.groupby("Cluster")[profile_columns].mean()

    print(profile.round(2))


    print("\n========== SPENDING BY PRODUCT ==========")

    product_columns = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]

    spending_profile = df.groupby("Cluster")[product_columns].mean()

    print(spending_profile.round(2))


    print("\n========== CAMPAIGN RESPONSE ==========")

    campaign_columns = [
        "AcceptedCmp1",
        "AcceptedCmp2",
        "AcceptedCmp3",
        "AcceptedCmp4",
        "AcceptedCmp5",
        "Response"
    ]

    campaign_profile = df.groupby("Cluster")[campaign_columns].mean() * 100

    print(campaign_profile.round(2))


# ============================================================
# 6. REMOVE TEMPORARY CLUSTER COLUMN
# ============================================================

df.drop(columns=["Cluster"], inplace=True)

print("\n\nCluster evaluation completed.")
