import os
import yfinance as yf
import pandas as pd

# Create folders
os.makedirs("data/csv", exist_ok=True)
os.makedirs("data/json", exist_ok=True)

print("=" * 50)
print("Institutional Trading AI")
print("=" * 50)

symbol = input("Enter NSE Stock Symbol (Example: MARICO.NS): ").strip().upper()

timeframes = {
    "5m": ("5d", "5m"),
    "15m": ("30d", "15m"),
    "1h": ("730d", "60m"),
    "1d": ("10y", "1d"),
}

for tf, (period, interval) in timeframes.items():

    print(f"\nDownloading {tf} data...")

    # Download data
    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=False
    )

    # Flatten MultiIndex columns (Yahoo Finance)
    if isinstance(df.columns, yf.pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Convert index into a Date column
    df = df.reset_index()

    # File names
    csv_file = f"data/csv/{symbol}_{tf}.csv"
    json_file = f"data/json/{symbol}_{tf}.json"

    # Save
    df.to_csv(csv_file, index=False)
    df.to_json(json_file, orient="records")

    print(f"Saved {csv_file}")
    print(f"Saved {json_file}")

print("\n✅ All downloads completed successfully!")