import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

engine = create_engine("postgresql://postgres:12345@localhost:5432/stockdb")

winners = pd.read_sql("""
SELECT season, "Stock"
FROM (
    SELECT 
        season,
        "Stock",
        RANK() OVER (PARTITION BY season ORDER BY AVG(season_return) DESC) AS rnk
    FROM seasonal_returns
    GROUP BY season, "Stock"
) t
WHERE rnk = 1;
""", engine)

prices = pd.read_sql("""
SELECT "Date","Stock","Close",season
FROM stock_seasons
ORDER BY "Date";
""", engine)

prices["Date"] = pd.to_datetime(prices["Date"])

capital = 100
history = []

for year in sorted(prices["Date"].dt.year.unique()):
    for season in ["Summer","Monsoon","Festive","YearEnd"]:

        try:
            stock = winners[winners["season"] == season]["Stock"].values[0]

            df = prices[
                (prices["Stock"] == stock) &
                (prices["Date"].dt.year == year) &
                (prices["season"] == season)
            ]

            if len(df) < 2:
                continue

            buy = float(df.iloc[0]["Close"])
            sell = float(df.iloc[-1]["Close"])

            capital *= (sell / buy)

            history.append([year, season, stock, buy, sell, capital])

        except:
            continue

result = pd.DataFrame(history, columns=[
    "Year","Season","Stock","BuyPrice","SellPrice","Capital"
])

result.to_csv(os.path.join(PROCESSED_DIR, "backtest_results.csv"), index=False)

print("✅ Backtest complete")
print("Final Capital:", round(capital,2))