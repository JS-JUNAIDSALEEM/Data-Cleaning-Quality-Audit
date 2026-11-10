
# Data Cleaning & Quality Audit

import pandas as pd
import numpy as np
import os


# ========================== CREATE SAMPLE DATASET ==========================

def create_sample_dataset():

    data = {
        "Customer": [" Ali ", "Sara", "AHMED", "Sara", None, "Ayesha", "Usman", "Fatima", "Hassan", "Sara", "Zara", "Bilal", "Hamza", "Noor", "Ali"],
        "Age": [25, 30, -1, 30, 22, None, 150, 28, 35, 30, 24, 29, 32, "unknown", 25],
        "City": ["Kasur", "Lahore", "KASUR", "Lahore", None, "Karachi", "lahore", "Islamabad", "Kasur", "Lahore", "Karachi", "ISLAMABAD", "Kasur", "Lahore", "Kasur"],
        "Purchase": [5000, None, 7000, None, 2500, 9000, -200, 4500, 6000, None, 8000, 3500, 70000, 5500, 5000],
        "Purchase_Date": ["2025-02-01", "2025/02/05", "2025-02-06", "2025/02/05", None, "invalid", "2025-02-10", "2025-03-01", "2025-03-05", "2025/02/05", "2025-03-10", "2025-03-12", "2025-03-15", None, "2025-02-01"]
    }

    return pd.DataFrame(data)

# ========================== FIND UNUSUAL PURCHASE VALUES ==========================

def find_purchase_outliers(purchase_values):

    purchase_values = pd.to_numeric(purchase_values, errors="coerce")

    # Ignore missing and negative purchase values
    valid_purchases = purchase_values[(purchase_values >= 0) & purchase_values.notna()]

    if len(valid_purchases) < 2:
        return pd.Series(False, index=purchase_values.index)

    q1 = valid_purchases.quantile(0.25)
    q3 = valid_purchases.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        ((purchase_values < lower_bound) | (purchase_values > upper_bound))
        & purchase_values.notna() & (purchase_values >= 0) )

    return outliers


# ========================== DATA CLEANING FUNCTION ==========================

def cleaned_customers(df_input):

    df = df_input.copy()
    initial_row_count = len(df)

# 1. Clean column names

    df.columns = (df.columns.astype("string").str.strip().str.lower().str.replace(" ", "_", regex=False))

# 2. Check required and unexpected columns

    required_columns = ["customer", "age", "city", "purchase", "purchase_date"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    unexpected_columns = [col for col in df.columns if col not in required_columns]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if unexpected_columns:
        raise ValueError(f"Unexpected columns: {unexpected_columns}")

# 3. Check original data

    missing_before = int(df_input.isna().sum().sum())
    missing_dates_before = int(df["purchase_date"].isna().sum())
    duplicate_before = int(df.duplicated().sum())

    # Calculate outliers from original purchase values

    before_outliers = find_purchase_outliers(df["purchase"])
    before_outlier_count = int(before_outliers.sum())

# 4. Clean customer and city names

    df["customer"] = (df["customer"].astype("string").str.strip().str.title())
    df["customer"] = df["customer"].replace("", np.nan)

    df["city"] = (df["city"].astype("string").str.strip().str.title())
    df["city"] = df["city"].replace("", np.nan)

    # Correct inconsistent city names
    df["city"] = df["city"].replace({
        "Kasur ": "Kasur",
        "Lahor": "Lahore",
        "Karachi ": "Karachi"})

# 5. Correct data types

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["purchase"] = pd.to_numeric(df["purchase"], errors="coerce")

# 6. Find invalid ages

    invalid_ages = ~df["age"].between(1, 120) & df["age"].notna()
    invalid_age_count = int(invalid_ages.sum())
    df.loc[invalid_ages, "age"] = np.nan

# 7. Find invalid purchases

    invalid_purchases = (df["purchase"] < 0) & df["purchase"].notna()
    invalid_purchase_count = int(invalid_purchases.sum())
    df.loc[invalid_purchases, "purchase"] = np.nan

# 8. Fix purchase dates

    original_dates = df["purchase_date"].astype("string").str.strip()
    original_dates = original_dates.replace("", pd.NA)

    df["purchase_date"] = pd.to_datetime(original_dates.str.replace("/", "-", regex=False), errors="coerce")

    invalid_dates = original_dates.notna() & df["purchase_date"].isna()
    invalid_date_count = int(invalid_dates.sum())

# 9. Remove duplicate records

    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    duplicates_removed = initial_row_count - len(df)

# 10. Handle missing values

    df["customer"] = df["customer"].fillna("Unknown")
    df["city"] = df["city"].fillna("Unknown")

    age_median = df["age"].median()
    purchase_mean = df["purchase"].mean()

    if pd.isna(age_median) or pd.isna(purchase_mean):
        raise ValueError("Not enough valid age or purchase values.")

    df["age"] = df["age"].fillna(age_median)
    df["purchase"] = df["purchase"].fillna(purchase_mean)

    # Missing purchase dates are not filled with fake dates.
    # They remain missing and are reported separately.

# 10. Count unusual purchase values

    after_outliers = find_purchase_outliers(df["purchase"])
    after_outlier_count = int(after_outliers.sum())

# 11. Check cleaned data

    missing_remaining = int(df.isna().sum().sum())
    duplicate_remaining = int(df.duplicated().sum())
    missing_dates_after = int(df["purchase_date"].isna().sum())

# 12. Create quality report

    report = {
        "Rows":                   [initial_row_count, len(df)],
        "Missing Values":         [missing_before, missing_remaining],
        "Missing Purchase Dates": [missing_dates_before, missing_dates_after],
        "Duplicate Records":      [duplicate_before, duplicate_remaining],
        "Duplicates Removed":     [0, duplicates_removed],
        "Invalid Ages":           [invalid_age_count, 0],
        "Invalid Purchases":      [invalid_purchase_count, 0],
        "Invalid Dates":          [invalid_date_count, 0],
        "Purchase Outliers":      [before_outlier_count, after_outlier_count]
    }

    quality_report = pd.DataFrame(report, index=["Before Cleaning", "After Cleaning"]).T

    return df, quality_report, after_outlier_count


# ========================== MAIN FUNCTION ==========================

def main():

    print("\n\n================ DATA CLEANING & QUALITY AUDIT ================\n")

# 1. Load sample dataset or user CSV

    file_path = input("Enter CSV file path (or press Enter for sample dataset): ").strip()

    if file_path:
        raw_df = pd.read_csv(file_path)
        print("\nUser CSV dataset loaded successfully.")
    else:
        raw_df = create_sample_dataset()
        print("\nSample dataset loaded successfully.")

# 2. BEFORE CLEANING

    print("\n\n=================== ORIGINAL DATASET ====================\n")
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

# 3. RUN DATA CLEANING

    cleaned_df, quality_report, outlier_count = cleaned_customers(raw_df)

# 4. VALIDATE CLEANED DATA

    print("\n\n============ DATA VALIDATION ============\n")

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

# 5. OUTLIER REPORT

    print("\n\n=========== PURCHASE OUTLIER ANALYSIS ===========\n")
    print("Total Unusual Purchase Values:", outlier_count)

    print("\nPurchase Outlier Records:")
    after_outliers = find_purchase_outliers(cleaned_df["purchase"])
    print(cleaned_df[after_outliers])

# 6. FINAL RESULTS

    print("\n\n================ CLEANED DATASET ===================\n")
    print(cleaned_df)

    print("\n\n=================== QUALITY REPORT =====================\n")
    print(quality_report)

# 6. SAVE OUTPUT FILES

    os.makedirs("output", exist_ok=True)

    cleaned_df.to_csv("output/cleaned_customers.csv", index=False)
    quality_report.to_csv("output/data_quality_report.csv")

    print("\n\n============ EXPORT STATUS ============\n")
    print("Cleaned dataset saved successfully.")
    print("Quality report saved successfully.")
    print("\n========== PROJECT COMPLETED ==========")


# ========================== RUN PROJECT ==========================

if __name__ == "__main__":

    try:
        main()
    except FileNotFoundError:
        print("\nError: CSV file not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("\nError: The CSV file is empty.")
    except pd.errors.ParserError:
        print("\nError: Unable to read the CSV file. Check its format.")
    except ValueError as error:
        print(f"\nData Error: {error}")
    except Exception as error:
        print(f"\nAn unexpected error occurred: {error}")
