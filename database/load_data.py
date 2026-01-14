import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:12345@localhost:5432/stockdb")

df = pd.read_csv("data/raw/nse_stocks_10y.csv")

df.to_sql("stock_prices", engine, if_exists="append", index=False)

print("✅ Data loaded into PostgreSQL")