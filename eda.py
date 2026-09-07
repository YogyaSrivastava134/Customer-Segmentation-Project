import pandas as pd
import matplotlib.pyplot as plt
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

output_folder = os.path.join(
    project_folder,
    "outputs"
)

os.makedirs(output_folder, exist_ok=True)

df = pd.read_csv(data_file)


# ============================================================
# 2. BASIC STATISTICS
# ============================================================

print("\n========== NUMERICAL SUMMARY ==========")

columns = [
    "Age",
    "Income",
    "TotalChildren",
    "TotalSpending",
    "TotalPurchases",
    "Recency",
    "NumWebVisitsMonth"
]

print(df[columns].describe())


# ============================================================
# 3. AGE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(df["Age"], bins=20)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "age_distribution.png"),
    dpi=300
)

plt.show()


# ============================================================
# 4. INCOME DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(df["Income"], bins=30)

plt.title("Customer Income Distribution")
plt.xlabel("Income")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "income_distribution.png"),
    dpi=300
)

plt.show()


# ============================================================
# 5. TOTAL SPENDING DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(df["TotalSpending"], bins=30)

plt.title("Customer Spending Distribution")
plt.xlabel("Total Spending")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "spending_distribution.png"),
    dpi=300
)

plt.show()


# ============================================================
# 6. TOTAL PURCHASES DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(df["TotalPurchases"], bins=25)

plt.title("Customer Purchase Frequency")
plt.xlabel("Total Purchases")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "purchase_distribution.png"),
    dpi=300
)

plt.show()


# ============================================================
# 7. PURCHASE CHANNELS
# ============================================================

channel_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

channel_totals = df[channel_columns].sum()

plt.figure(figsize=(8, 5))

plt.bar(
    ["Web", "Catalog", "Store"],
    channel_totals
)

plt.title("Purchases by Channel")
plt.xlabel("Channel")
plt.ylabel("Total Purchases")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "purchase_channels.png"),
    dpi=300
)

plt.show()


# ============================================================
# 8. PRODUCT CATEGORY SPENDING
# ============================================================

product_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

product_totals = df[product_columns].sum()

product_names = [
    "Wines",
    "Fruits",
    "Meat",
    "Fish",
    "Sweets",
    "Gold"
]

plt.figure(figsize=(9, 5))

plt.bar(
    product_names,
    product_totals
)

plt.title("Spending by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Spending")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "product_spending.png"),
    dpi=300
)

plt.show()


# ============================================================
# 9. CORRELATION MATRIX
# ============================================================

correlation_columns = [
    "Age",
    "Income",
    "Recency",
    "TotalSpending",
    "TotalPurchases",
    "NumWebVisitsMonth",
    "TotalChildren"
]

correlation = df[correlation_columns].corr()

print("\n========== CORRELATION MATRIX ==========")
print(correlation.round(2))


plt.figure(figsize=(9, 7))

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(correlation_columns)),
    correlation_columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation_columns)),
    correlation_columns
)

plt.title("Customer Feature Correlation Matrix")

plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "correlation_matrix.png"),
    dpi=300
)

plt.show()


print("\nEDA completed successfully!")
print("Charts saved to:")
print(output_folder)
