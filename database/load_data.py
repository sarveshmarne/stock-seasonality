import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

engine = create_engine("postgresql://postgres:12345@localhost:5432/stockdb")

df = pd.read_csv(os.path.join(RAW_DIR, "nse_stocks_10y.csv"))

df.to_sql("stock_prices", engine, if_exists="append", index=False)

print("✅ Data loaded into PostgreSQL")