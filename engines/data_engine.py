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

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Remove duplicate columns if any
        df = df.loc[:, ~df.columns.duplicated()]

        return df