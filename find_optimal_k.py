import pandas as pd
import numpy as np
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
    "clustering_features.csv"
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

print("Dataset shape:", df.shape)


# ============================================================
# 3. STANDARDIZE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(df)

print("\nFeatures standardized successfully.")
print("Scaled data shape:", X_scaled.shape)


# ============================================================
# 4. TEST DIFFERENT VALUES OF K
# ============================================================

k_values = range(2, 11)

inertias = []
silhouette_scores = []


for k in k_values:

    # Create K-Means model
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    # Fit model
    labels = kmeans.fit_predict(X_scaled)

    # Store inertia
    inertias.append(kmeans.inertia_)

    # Calculate silhouette score
    score = silhouette_score(
        X_scaled,
        labels
    )

    silhouette_scores.append(score)

    print(
        f"K = {k:2} | "
        f"Inertia = {kmeans.inertia_:10.2f} | "
        f"Silhouette Score = {score:.4f}"
    )


# ============================================================
# 5. FIND BEST SILHOUETTE SCORE
# ============================================================

best_k = k_values[
    np.argmax(silhouette_scores)
]

best_score = max(silhouette_scores)

print("\n========== BEST SILHOUETTE RESULT ==========")

print("Best K:", best_k)
print("Best Silhouette Score:", round(best_score, 4))


# ============================================================
# 6. ELBOW CURVE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    list(k_values),
    inertias,
    marker="o"
)

plt.title("Elbow Method for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")

plt.xticks(list(k_values))

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "elbow_curve.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 7. SILHOUETTE SCORE CURVE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    list(k_values),
    silhouette_scores,
    marker="o"
)

plt.title("Silhouette Score for Different K Values")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")

plt.xticks(list(k_values))

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "silhouette_scores.png"
    ),
    dpi=300
)

plt.show()


print("\n========== COMPLETED ==========")

print("Charts saved to:")
print(output_folder)
