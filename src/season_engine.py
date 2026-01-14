import pandas as pd
from sqlalchemy import create_engine

# Change password
engine = create_engine("postgresql://postgres:12345@localhost:5432/stockdb")

# Load stock data
query = 'SELECT "Date","Open","High","Low","Close","Volume","Stock" FROM stock_prices'
df = pd.read_sql(query, engine)

# Convert date
df["Date"] = pd.to_datetime(df["Date"])
df["month"] = df["Date"].dt.month


# Season logic
def get_season(month):
    if month in [3,4,5,6]:
        return "Summer"
    elif month in [7,8,9]:
        return "Monsoon"
    elif month in [10,11]:
        return "Festive"
    else:
        return "YearEnd"

df["season"] = df["month"].apply(get_season)

# Save new table
df.to_sql("stock_seasons", engine, if_exists="replace", index=False)

print("✅ Season-tagged data saved to stock_seasons")