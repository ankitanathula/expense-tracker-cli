# test_summarize.py
import pandas as pd
from expense_tracker import summarize

def test_summarize_monthly_and_category():
    # 1. Build a tiny DataFrame
    data = {
        "date": ["2025-07-01", "2025-07-02", "2025-08-01"],
        "amount": [10.0, 20.0, 30.0],
        "category": ["food", "food", "travel"]
    }
    df = pd.DataFrame(data)

    # 2. Run summarize with categories
    monthly, category = summarize(df, by_category=True)

    # 3. Check monthly sums and means
    #    July sum = 10 + 20 = 30, mean = 15
    #    August sum = 30, mean = 30
    july = monthly.loc[pd.Period("2025-07", "M")]
    august = monthly.loc[pd.Period("2025-08", "M")]

    assert july["sum"] == 30.0
    assert july["mean"] == 15.0
    assert august["sum"] == 30.0
    assert august["mean"] == 30.0

    # 4. Check category totals
    assert category["food"] == 30.0
    assert category["travel"] == 30.0
