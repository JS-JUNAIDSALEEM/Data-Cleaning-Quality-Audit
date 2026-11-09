# Data Cleaning & Quality Audit

import pandas as pd
import numpy as np
import os



# CREATE DATASET

data = {
    "Customer": [" Ali ", "Sara", "AHMED", "Sara", None, "Ayesha", "Usman", "Fatima", "Hassan", "Sara", "Zara", "Bilal", "Hamza", "Noor", "Ali"],
    "Age": [25, 30, -1, 30, 22, None, 150, 28, 35, 30, 24, 29, 32, "unknown", 25],
    "City": ["Kasur", "Lahore", "KASUR", "Lahore", None, "Karachi", "lahore", "Islamabad", "Kasur", "Lahore", "Karachi", "ISLAMABAD", "Kasur", "Lahore", "Kasur"],
    "Purchase": [5000, None, 7000, None, 2500, 9000, -200, 4500, 6000, None, 8000, 3500, 70000, 5500, 5000],
    "Purchase_Date": ["2025-02-01", "2025/02/05", "2025-02-06", "2025/02/05", None, "invalid", "2025-02-10", "2025-03-01", "2025-03-05", "2025/02/05", "2025-03-10", "2025-03-12", "2025-03-15", None, "2025-02-01"]
}

raw_df = pd.DataFrame(data)

# ========================== BEFORE CLEANING ==========================

print("\n========== ORIGINAL DATASET ==========\n")

print(raw_df)

print("\nDataset Shape:")
print(raw_df.shape)

print("\nData Types:")
print(raw_df.dtypes)

print("\nMissing Values:")
print(raw_df.isna().sum())

missing_percentage = (raw_df.isna().mean() * 100).round(2)

print("\nMissing Value Percentage:")
print(missing_percentage)


# ========================== DATA CLEANING FUNCTION ==========================

def cleaned_customers(df_input):

    df = df_input.copy()

    initial_row_count = len(df)

# 1. Standardize column names

    df.columns = (
        df.columns.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

# 2. Clean customer names

    df["customer"] = (
        df["customer"].astype("string")
        .str.strip()
        .str.title()
    )

    df["customer"] = df["customer"].replace("", np.nan)

# 3. Clean city names

    df["city"] = (
        df["city"].astype("string")
        .str.strip()
        .str.title()
    )

    df["city"] = df["city"].replace("", np.nan)

    # Correct inconsistent city names

    df["city"] = df["city"].replace({
        "Kasur ": "Kasur",
        "Lahor": "Lahore",
        "Karachi ": "Karachi"
    })

# 4. Correct data types

    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    df["purchase"] = pd.to_numeric(
        df["purchase"], errors="coerce"
    )

# 5. Detect invalid age values

    invalid_ages = (
        (~df["age"].between(1, 120))
        & df["age"].notna()
    )

    invalid_age_count = int(invalid_ages.sum())

    df.loc[invalid_ages, "age"] = np.nan

# 6. Detect invalid purchase values

    invalid_purchases = (
        (df["purchase"] < 0)
        & df["purchase"].notna()
    )

    invalid_purchase_count = int(invalid_purchases.sum())

    df.loc[invalid_purchases, "purchase"] = np.nan

# 7. Correct purchase date format

    original_dates = df["purchase_date"].copy()

    df["purchase_date"] = (
        df["purchase_date"].astype("string")
        .str.replace("/", "-", regex=False)
    )

    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"], errors="coerce"
    )

    invalid_dates = (
        original_dates.notna()
        & df["purchase_date"].isna()
    )

    invalid_date_count = int(invalid_dates.sum())

# 8. Find duplicate records

    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    duplicates_removed = initial_row_count - len(df)

# 9. Handle missing values

    df["customer"] = df["customer"].fillna("Unknown")
    df["city"] = df["city"].fillna("Unknown")
    df["age"] = df["age"].fillna(df["age"].median())
    df["purchase"] = df["purchase"].fillna(df["purchase"].mean())

# 10. Detect purchase outliers using IQR

    q1 = df["purchase"].quantile(0.25)
    q3 = df["purchase"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        (df["purchase"] < lower_bound)
        | (df["purchase"] > upper_bound)
    )

    outlier_count = int(outliers.sum())

    # 11. Validate cleaned data

    missing_remaining = int(df.isna().sum().sum())
    duplicate_remaining = int(df.duplicated().sum())

    # 12. Create quality report

    report = {
        "Rows": [initial_row_count, len(df)],

        "Missing Values": [int(df_input.isna().sum().sum()), missing_remaining],

        "Duplicate Records": [duplicate_count,duplicate_remaining],

        "Invalid Ages": [invalid_age_count, 0],

        "Invalid Purchases": [invalid_purchase_count, 0],

        "Invalid Dates": [invalid_date_count, int(df["purchase_date"].isna().sum())],

        "Purchase Outliers": [outlier_count, outlier_count]
    }

    quality_report = pd.DataFrame(report, index=["Before Cleaning", "After Cleaning"]).T

    return df, quality_report, outlier_count


# ========================== RUN CLEANING ==========================

cleaned_df, quality_report, outlier_count = cleaned_customers(raw_df)


# ========================== VALIDATE CLEANED DATA ==========================

print("\n========== DATA VALIDATION ==========\n")

assert cleaned_df["customer"].notna().all()

assert cleaned_df["city"].notna().all()

assert cleaned_df["age"].between(1, 120).all()

assert (cleaned_df["purchase"] >= 0).all()

assert not cleaned_df.duplicated().any()

print("Customer Validation: PASSED")
print("City Validation: PASSED")
print("Age Validation: PASSED")
print("Purchase Validation: PASSED")
print("Duplicate Validation: PASSED")


# ========================== OUTLIER REPORT ==========================

print("\n========== OUTLIER ANALYSIS ==========\n")

print("Total Purchase Outliers:", outlier_count)
print("\nPurchase Outlier Records:")

q1 = cleaned_df["purchase"].quantile(0.25)
q3 = cleaned_df["purchase"].quantile(0.75)

iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print(
    cleaned_df[
        (cleaned_df["purchase"] < lower_bound)
        | (cleaned_df["purchase"] > upper_bound)
    ]
)


# ========================== FINAL RESULTS ==========================

print("\n========== CLEANED DATASET ==========\n")
print(cleaned_df)

print("\n========== QUALITY REPORT ==========\n")
print(quality_report)


# ========================== EXPORT FILES ==========================

os.makedirs("output", exist_ok=True)

cleaned_df.to_csv(
    "output/cleaned_customers.csv",
    index=False
)

quality_report.to_csv(
    "output/data_quality_report.csv"
)

print("\n========== EXPORT STATUS ==========\n")

print("Cleaned dataset saved successfully.")
print("Quality report saved successfully.")

print("\n========== PROJECT COMPLETED ==========")