import pandas as pd
import os

dataset_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project\dataset"
file_path = os.path.join(dataset_folder, "customer_segmentation.csv")

df = pd.read_csv(file_path)

# Convert date
df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], dayfirst=True)

print("\n========== MISSING INCOME RECORDS ==========")

missing_income = df[df["Income"].isnull()]

print(missing_income[
    ["ID", "Year_Birth", "Education", "Marital_Status", "Income",
     "Kidhome", "Teenhome", "Recency"]
].to_string(index=False))


print("\n========== EXTREME INCOME RECORDS ==========")

high_income = df[df["Income"] > 200000]

print(high_income[
    ["ID", "Year_Birth", "Education", "Marital_Status", "Income",
     "MntWines", "MntMeatProducts", "MntGoldProds"]
].to_string(index=False))


print("\n========== EXTREME AGE RECORDS ==========")

old_customers = df[df["Year_Birth"] < 1940]

print(old_customers[
    ["ID", "Year_Birth", "Education", "Marital_Status", "Income",
     "MntWines", "MntMeatProducts", "MntGoldProds"]
].to_string(index=False))


print("\n========== ZERO / VERY LOW INCOME ==========")

print(
    df[df["Income"] < 10000][
        ["ID", "Year_Birth", "Education", "Marital_Status", "Income"]
    ].to_string(index=False)
)


print("\n========== NUMERICAL OUTLIER SUMMARY ==========")

numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < lower) | (df[column] > upper)
    ]

    print(
        f"{column:25} "
        f"Outliers: {len(outliers):4} | "
        f"Lower: {lower:10.2f} | "
        f"Upper: {upper:10.2f}"
    )
