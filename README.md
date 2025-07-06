# Expense Tracker CLI

A command-line tool to import and analyze expense data from bank-statement CSV files, providing summarized reports by month and category.

---

## 🚩 Problem

Manually sifting through multiple CSV exports of bank statements to understand monthly and category-based spending is time-consuming and error-prone.

## 💡 Solution

Provide a simple CLI that:
- Imports one or more CSV files
- Parses date, amount, (optional) category columns
- Summarizes total and average spending per month
- Breaks down spending by category
- Exports the summary report as CSV or prints it to the console

---

## 🎯 MVP Features

1. **Import CSVs**: Accept one or more file paths as arguments.
2. **Parse Data**: Read CSVs, extract date, amount, (optional) category columns.
3. **Monthly Summary**: Compute total spending and average per month.
4. **Category Breakdown**: If category data exists, group and sum by category.
5. **Output**: Print tables to console and (optionally) export summary as a new CSV file.

---

## ⚙️ Installation

```bash
git clone https://github.com/ankitanathula/expense-tracker-cli.git
cd expense-tracker-cli
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
