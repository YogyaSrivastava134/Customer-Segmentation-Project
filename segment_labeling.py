import pandas as pd
import os


# ============================================================
# 1. PATHS
# ============================================================

project_folder = r"C:\Users\yogya\OneDrive\Desktop\NIET\Semester VII\Thinerax\Customer Segmentation Project"

input_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segments.csv"
)

output_file = os.path.join(
    project_folder,
    "dataset",
    "customer_segments_final.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(input_file)


# ============================================================
# 3. ASSIGN BUSINESS SEGMENT NAMES
# ============================================================

segment_names = {
    0: "Premium Customers",
    1: "Emerging Customers",
    2: "Growth Customers"
}

df["Segment"] = df["Cluster"].map(segment_names)


# ============================================================
# 4. DISPLAY SEGMENT SUMMARY
# ============================================================

print("\n========== FINAL CUSTOMER SEGMENTS ==========")

summary = (
    df.groupby(["Cluster", "Segment"])
      .size()
      .reset_index(name="Customers")
)

summary["Percentage"] = (
    summary["Customers"] / len(df) * 100
)

print(
    summary.to_string(index=False)
)


# ============================================================
# 5. SAVE FINAL DATASET
# ============================================================

df.to_csv(
    output_file,
    index=False
)

print("\nFinal segmented dataset saved to:")
print(output_file)
