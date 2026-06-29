import yfinance as yf
import pandas as pd


class DataEngine:

    def __init__(self):
        print("✅ Data Engine Ready")

    def get_data(self, symbol, period="1y", interval="1d"):

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False
        )

        # Check if data exists
        if df.empty:
            raise ValueError(f"No data found for {symbol}")

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # Convert price columns to numeric
        numeric_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df