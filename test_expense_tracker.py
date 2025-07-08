# test_expense_tracker.py
import pandas as pd
from expense_tracker import load_data

def test_load_data(tmp_path):
    # create two tiny CSV files
    csv1 = tmp_path / "f1.csv"
    csv2 = tmp_path / "f2.csv"
    csv1.write_text("date,amount,category\n2025-07-01,10.0,food\n")
    csv2.write_text("date,amount,category\n2025-07-02,20.0,travel\n")

    # run load_data on them
    df = load_data([str(csv1), str(csv2)])

    # check that it merged correctly
    assert list(df.columns) == ["date", "amount", "category"]
    assert len(df) == 2

    # check the values row by row
    row0 = df.iloc[0]
    assert row0["amount"] == 10.0
    assert row0["category"] == "food"

    row1 = df.iloc[1]
    assert row1["amount"] == 20.0
    assert row1["category"] == "travel"
