import yfinance as yf
import pandas as pd
import os

stocks = [
    "DMART.NS","TRENT.NS","TITAN.NS","RELIANCE.NS","ITC.NS",
    "HINDUNILVR.NS","NESTLEIND.NS",
    "MARUTI.NS","M&M.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS",
    "HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","AXISBANK.NS",
    "TCS.NS","INFY.NS","WIPRO.NS",
    "LT.NS","ULTRACEMCO.NS","ASIANPAINT.NS","PIDILITIND.NS"
]

all_data = []

for stock in stocks:
    try:
        print("Downloading", stock)
        df = yf.download(stock, start="2015-01-01", end="2025-01-01", progress=False)

        if df.empty:
            print("❌ No data for", stock)
            continue

        df.reset_index(inplace=True)
        df["Stock"] = stock
        all_data.append(df)

    except Exception as e:
        print("❌ Error downloading", stock, e)

# Make sure folder exists
os.makedirs("data/raw", exist_ok=True)

final_df = pd.concat(all_data)
final_df.to_csv("data/raw/nse_stocks_10y.csv", index=False)

print("✅ Saved → data/raw/nse_stocks_10y.csv")
print("Rows:", len(final_df))
