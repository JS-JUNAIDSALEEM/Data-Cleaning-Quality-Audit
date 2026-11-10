# Data Cleaning & Quality Audit Tests

import unittest
import pandas as pd

from main import cleaned_customers

# TEST DATASET

def create_test_data():

    data = {
        "Customer": [" Ali ", "Sara", "AHMED", "Sara", "Bilal"],
        "Age": [25, 30, -1, None, 35],
        "City": ["Kasur", "Lahore", "KASUR", "Lahore", "Karachi"],
        "Purchase": [5000, 3000, -200, None, 7000],
        "Purchase_Date": ["2025-02-01", "2025/02/05", "2025-02-06", None, "invalid"]
    }

    return pd.DataFrame(data)

# TEST DATA CLEANING

class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        self.raw_df = create_test_data()
        self.cleaned_df, self.quality_report, self.outlier_count = (cleaned_customers(self.raw_df))

# Test 1: Check cleaned column names

    def test_column_names(self):
        self.assertEqual(
            list(self.cleaned_df.columns),
            ["customer", "age", "city", "purchase", "purchase_date"] )

# Test 2: Check missing customer and city values

    def test_missing_text_values(self):
        self.assertFalse(self.cleaned_df["customer"].isna().any())
        self.assertFalse(self.cleaned_df["city"].isna().any())

# Test 3: Check invalid ages

    def test_invalid_ages(self):
        self.assertTrue(self.cleaned_df["age"].between(1, 120).all())

# Test 4: Check invalid purchases

    def test_invalid_purchases(self):
        self.assertTrue((self.cleaned_df["purchase"] >= 0).all())

# Test 5: Check duplicate records

    def test_duplicates(self):
        self.assertFalse(self.cleaned_df.duplicated().any())

# Test 6: Check missing dates are reported

    def test_missing_dates(self):
        self.assertEqual(self.cleaned_df["purchase_date"].isna().sum(), 2)
        self.assertEqual(self.quality_report.loc["Missing Purchase Dates", "After Cleaning"], 2)

# Test 7: Check quality report

    def test_quality_report(self):
        self.assertIn("Invalid Ages", self.quality_report.index)
        self.assertIn("Invalid Purchases", self.quality_report.index)
        self.assertIn("Purchase Outliers", self.quality_report.index)

# RUN TESTS

if __name__ == "__main__":
    unittest.main()