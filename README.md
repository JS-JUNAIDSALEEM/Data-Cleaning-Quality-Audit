# Data Cleaning & Quality Audit

## Project Overview

Data Cleaning & Quality Audit is a Python project that helps identify and fix common problems in a dataset.

The project uses Pandas and NumPy to find missing values, duplicate records, invalid values, inconsistent formatting, and possible outliers.

It also validates the cleaned data and generates a report to compare the dataset before and after cleaning.

## Features

- Load and inspect customer data.
- Find missing values.
- Detect duplicate records.
- Clean customer names and city names.
- Correct data types.
- Detect invalid ages and purchase amounts.
- Handle missing values.
- Convert date columns into the correct format.
- Detect possible outliers using the IQR method.
- Validate cleaned data using assertions.
- Generate a before-and-after quality report.
- Export cleaned data and reports into CSV files.

## Technologies Used

- Python
- Pandas
- NumPy
- CSV File Handling
- Data Validation

## Project Structure

```text
Data-Cleaning-Quality-Audit/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── output/
    ├── cleaned_customers.csv
    └── data_quality_report.csv
```

## How to Run

**Step 1: Clone the repository**

```bash
git clone https://github.com/JS-JUNAIDSALEEM/Data-Cleaning-Quality-Audit.git
```

**Step 2: Open the project folder**

```bash
cd Data-Cleaning-Quality-Audit
```

**Step 3: Install the required libraries**

```bash
pip install -r requirements.txt
```

**Step 4: Run the project**

```bash
python main.py
```

## Output Files

After running the project, an output folder is created automatically.

**1. cleaned_customers.csv**

Contains customer data after cleaning and validation.

**2. data_quality_report.csv**

Contains a comparison of data quality before and after cleaning, including missing values, duplicates, invalid values, and outliers.

## Data Cleaning Process

The project follows these main steps:

1. Inspect the original dataset.
2. Check missing values and their percentages.
3. Standardize column names and text formatting.
4. Correct numeric and date data types.
5. Detect invalid ages and purchase amounts.
6. Remove duplicate records.
7. Fill missing values.
8. Detect possible outliers using IQR.
9. Validate the cleaned dataset.
10. Export the cleaned data and quality report.

## What I Learned

While working on this project, I practiced:

- Working with Pandas DataFrames.
- Handling missing and duplicate values.
- Cleaning inconsistent text.
- Converting data types.
- Detecting invalid values.
- Using the IQR method to find outliers.
- Applying data validation with assertions.
- Generating reports and exporting CSV files.

## Future Improvements

- Allow users to upload their own datasets.
- Add more data validation rules.
- Support multiple dataset formats.
- Create data quality charts.
- Build a simple user interface.

## Author

### Junaid Saleem

- **GitHub:** [JS-JUNAIDSALEEM](https://github.com/JS-JUNAIDSALEEM)
- **LinkedIn:** [Junaid Saleem](https://www.linkedin.com/in/junaid-saleem-developer/)