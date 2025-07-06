#!/usr/bin/env python3
import argparse
import pandas as pd
from tabulate import tabulate

def load_data(files):
    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs, ignore_index=True)

def summarize(df, by_category=False):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].agg(['sum', 'mean'])
    category = None
    if by_category and 'category' in df.columns:
        category = df.groupby('category')['amount'].sum()
    return monthly, category

def main():
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
