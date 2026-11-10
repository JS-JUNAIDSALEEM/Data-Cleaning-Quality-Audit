# Data Cleaning & Quality Audit

## Project Overview

Data Cleaning & Quality Audit is a Python project that helps the users to identify and fix common problems in a dataset.

The project uses Pandas and NumPy to find missing values, duplicate records, invalid values, inconsistent formatting, and possible outliers.

Users can clean the sample customer dataset or provide their own CSV file. The project also validates the cleaned data and generates a report to compare data quality before and after cleaning.

## Features

- Load and inspect customer data.
- Load a sample dataset or a user-provided CSV file.
- Find missing values.
- Detect duplicate records.
- Clean customer names and city names.
- Correct data types.
- Detect invalid ages and purchase amounts.
- Handle missing values.
- Convert date columns into the correct format.
- Report missing and invalid dates separately.
- Detect possible outliers using the IQR method.
- Validate cleaned data using assertions.
- Generate a before-and-after quality report.
- Export cleaned data and reports into CSV files.
- Check dataset columns and display errors for incorrect input.

## Technologies Used

- Python
- Pandas
- NumPy
- CSV File Handling
- Data Validation
- Unit Testing

## Project Structure

```text
Data-Cleaning-Quality-Audit/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── tests/
│   └── test_analysis.py
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

Press Enter to use the sample dataset, or enter the path of your own CSV file.

Your CSV file must contain these five columns:

- Customer
- Age
- City
- Purchase
- Purchase_Date

## Unit Testing

The project uses Python's built-in `unittest` module to test the data cleaning function.

Run the tests using this command:

```bash
py -m unittest tests/test_analysis.py -v
```

The tests check:

- Standardized column names.
- Missing customer and city values.
- Invalid age values.
- Invalid purchase values.
- Duplicate records.
- Missing purchase dates.
- Quality report fields.

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
7. Fill missing customer, city, age, and purchase values.
8. Keep missing purchase dates and report them separately.
9. Detect possible outliers using IQR.
10. Validate the cleaned dataset.
11. Generate the quality report and export CSV files.

## What I Learned

While working on this project, I practiced:

- Working with Pandas DataFrames.
- Handling missing and duplicate values.
- Cleaning inconsistent text.
- Converting data types.
- Detecting invalid values.
- Using the IQR method to find outliers.
- Applying data validation with assertions.
- Writing basic unit tests using unittest.
- Generating reports and exporting CSV files.

## Future Improvements

- Add more data validation rules.
- Support more dataset formats.
- Create data quality charts.
- Build a simple user interface.
- Add more automated tests.

## Author

### Junaid Saleem

- **GitHub:** [JS-JUNAIDSALEEM](https://github.com/JS-JUNAIDSALEEM)
- **LinkedIn:** [Junaid Saleem](https://www.linkedin.com/in/junaid-saleem-developer/)