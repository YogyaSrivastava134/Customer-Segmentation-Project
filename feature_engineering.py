import pandas as pd
import os

# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

project_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project"

data_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segmentation_cleaned.csv"
)

df = pd.read_csv(data_file)


# ============================================================
# 2. FINAL CLUSTERING FEATURES
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
# 3. CHECK FOR MISSING VALUES
# ============================================================

print("\n========== MISSING VALUES ==========")

print(X.isnull().sum())


# ============================================================
# 4. FEATURE LIST
# ============================================================

print("\n========== FINAL CLUSTERING FEATURES ==========")

for i, feature in enumerate(features, start=1):
    print(f"{i:2}. {feature}")


# ============================================================
# 5. FEATURE STATISTICS
# ============================================================

print("\n========== FEATURE STATISTICS ==========")

print(X.describe().round(2))


# ============================================================
# 6. CORRELATION MATRIX
# ============================================================

print("\n========== FINAL FEATURE CORRELATION ==========")

print(X.corr().round(2))


# ============================================================
# 7. SAVE FINAL CLUSTERING DATASET
# ============================================================

output_file = os.path.join(
    project_folder,
    "dataset",
    "clustering_features.csv"
)

X.to_csv(output_file, index=False)

print("\nFinal clustering dataset saved to:")
print(output_file)
