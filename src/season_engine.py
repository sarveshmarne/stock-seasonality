import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine("postgresql://postgres:12345@localhost:5432/stockdb")

query = 'SELECT "Date","Open","High","Low","Close","Volume","Stock" FROM stock_prices'
df = pd.read_sql(query, engine)

df["Date"] = pd.to_datetime(df["Date"])
df["month"] = df["Date"].dt.month

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

# IMPORTANT: Don't drop table because view depends on it
df.to_sql("stock_seasons", engine, if_exists="replace", index=False)

print("✅ Season-tagged data saved to stock_seasons")