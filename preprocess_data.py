import pandas as pd
import os

# ============================================================
# 1. LOAD DATA
# ============================================================

dataset_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project\dataset"

input_file = os.path.join(
    dataset_folder,
    "customer_segmentation.csv"
)

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)


# ============================================================
# 2. REMOVE CONSTANT COLUMNS
# ============================================================

df = df.drop(columns=[
    "Z_CostContact",
    "Z_Revenue"
])


# ============================================================
# 3. REMOVE INVALID BIRTH YEARS
# ============================================================

df = df[df["Year_Birth"] >= 1940].copy()


# ============================================================
# 4. HANDLE INVALID INCOME
# ============================================================

# Treat 666666 as an invalid income value
df.loc[df["Income"] == 666666, "Income"] = None

# Fill missing income values using the median
median_income = df["Income"].median()

df["Income"] = df["Income"].fillna(median_income)


# ============================================================
# 5. CONVERT CUSTOMER DATE
# ============================================================

df["Dt_Customer"] = pd.to_datetime(
    df["Dt_Customer"],
    dayfirst=True
)


# ============================================================
# 6. CREATE AGE
# ============================================================

reference_year = 2014

df["Age"] = reference_year - df["Year_Birth"]


# ============================================================
# 7. CREATE TOTAL CHILDREN
# ============================================================

df["TotalChildren"] = (
    df["Kidhome"] +
    df["Teenhome"]
)


# ============================================================
# 8. CREATE TOTAL SPENDING
# ============================================================

spending_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

df["TotalSpending"] = df[spending_columns].sum(axis=1)


# ============================================================
# 9. CREATE TOTAL PURCHASES
# ============================================================

purchase_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

df["TotalPurchases"] = df[purchase_columns].sum(axis=1)


# ============================================================
# 10. CUSTOMER TENURE
# ============================================================

reference_date = pd.Timestamp("2014-06-30")

df["CustomerTenureDays"] = (
    reference_date - df["Dt_Customer"]
).dt.days


# ============================================================
# 11. SAVE CLEANED DATASET
# ============================================================

output_file = os.path.join(
    dataset_folder,
    "customer_segmentation_cleaned.csv"
)

df.to_csv(output_file, index=False)


# ============================================================
# 12. SUMMARY
# ============================================================

print("\n========== CLEANING SUMMARY ==========")

print("Final dataset shape:", df.shape)

print("Missing income:", df["Income"].isnull().sum())

print("Minimum age:", df["Age"].min())
print("Maximum age:", df["Age"].max())

print("Median income:", df["Income"].median())

print("\nNew features:")
print([
    "Age",
    "TotalChildren",
    "TotalSpending",
    "TotalPurchases",
    "CustomerTenureDays"
])

print("\nCleaned dataset saved to:")
print(output_file)
