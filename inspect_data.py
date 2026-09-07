import pandas as pd
import os

dataset_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project\dataset"
file_path = os.path.join(dataset_folder, "customer_segmentation.csv")

# Load dataset
df = pd.read_csv(file_path)

print("\n========== BASIC INFORMATION ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n========== UNIQUE VALUES ==========")

print("\nEducation:")
print(df["Education"].value_counts())

print("\nMarital Status:")
print(df["Marital_Status"].value_counts())

print("\n========== INCOME ==========")
print("Missing:", df["Income"].isnull().sum())
print("Minimum:", df["Income"].min())
print("Maximum:", df["Income"].max())
print("Median:", df["Income"].median())

print("\n========== YEAR OF BIRTH ==========")
print("Minimum:", df["Year_Birth"].min())
print("Maximum:", df["Year_Birth"].max())

print("\nCustomers born before 1940:")
print(df[df["Year_Birth"] < 1940][["ID", "Year_Birth", "Income"]].to_string(index=False))

print("\n========== CUSTOMER DATE ==========")
df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], dayfirst=True)

print("Earliest:", df["Dt_Customer"].min())
print("Latest:", df["Dt_Customer"].max())

print("\n========== SPENDING ==========")

spending_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

print(df[spending_columns].describe())

print("\n========== PURCHASE CHANNELS ==========")

purchase_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases"
]

print(df[purchase_columns].describe())

print("\n========== CAMPAIGN RESPONSE ==========")

campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response"
]

for column in campaign_columns:
    print(f"{column}: {df[column].sum()} customers")

print("\n========== CONSTANT COLUMNS ==========")

for column in df.columns:
    if df[column].nunique() == 1:
        print(column, "->", df[column].unique()[0])
