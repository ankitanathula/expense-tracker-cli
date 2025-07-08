#!/usr/bin/env python3
import argparse
import pandas as pd
from tabulate import tabulate

def load_data(files):
    """
    Read one or more CSV files and return them as a single DataFrame.

    Args:
        files (list of str): Paths to CSV files to load.

    Returns:
        pandas.DataFrame: All input files concatenated row-wise, with a fresh integer index.

    Examples:
        >>> # If you have 'jan.csv' and 'feb.csv' each with date and amount columns
        >>> dfs = load_data(['jan.csv', 'feb.csv'])
        >>> isinstance(dfs, pandas.DataFrame)
        True
        >>> dfs.shape[0]  # number of rows should equal sum of both files’ rows
        42
    """
    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def summarize(df, by_category=False):
    """
    Compute monthly totals and averages, and optionally a category breakdown.

    Args:
        df (pandas.DataFrame): Must contain a 'date' column parseable by pandas, and an 'amount' column.
        by_category (bool, optional): If True and a 'category' column exists, also return totals per category. Defaults to False.

    Returns:
        tuple:
            - monthly (pandas.DataFrame): Indexed by Period('M'), with 'sum' and 'mean' of the 'amount' column.
            - category (pandas.Series or None): If requested, total amount per category; otherwise None.

    Examples:
        
    """
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].agg(['sum', 'mean'])
    category = None
    if by_category and 'category' in df.columns:
        category = df.groupby('category')['amount'].sum()
    return monthly, category


def main():
    """
    Parse CLI arguments, load data, summarize it, print tables, and optionally save CSV.

    Command-line interface:
      expense-tracker FILE [FILE ...] [--category] [--output OUT]

    Positional arguments:
      files          One or more CSV file paths.

    Optional flags:
      --category     Include a category breakdown if the CSVs have a 'category' column.
      --output OUT   Path to write the monthly summary as a CSV.

    Behavior:
      1. Load and merge all CSVs.
      2. Compute monthly totals and averages.
      3. Print a GitHub-style table of the monthly summary.
      4. If --category, print the total spent per category.
      5. If --output, save the monthly summary CSV and report where it was saved.

    Examples:
        # Summarize two files, show category totals, and save to 'out.csv'
        $ python expense-tracker.py jan.csv feb.csv --category --output out.csv
        # Output will look like a GitHub-style table in your terminal
    """
    parser = argparse.ArgumentParser(
        prog='expense-tracker',
        description='Import and summarize expense CSVs.'
    )
    parser.add_argument('files', nargs='+', help='CSV file paths.')
    parser.add_argument(
        '--category', action='store_true',
        help='Include category breakdown.'
    )
    parser.add_argument(
        '--output', metavar='OUT',
        help='Optional path to save summary CSV.'
    )
    args = parser.parse_args()

    df = load_data(args.files)
    monthly, category = summarize(df, by_category=args.category)

    print('\nMonthly Summary:')
    print(tabulate(monthly, headers='keys', tablefmt='github'))

    if category is not None:
        print('\nCategory Breakdown:')
        print(tabulate(
            category.reset_index().values,
            headers=['Category', 'Total'],
            tablefmt='github'
        ))

    if args.output:
        monthly.to_csv(args.output)
        print(f'\nSummary saved to {args.output}')

if __name__ == '__main__':
    main()
