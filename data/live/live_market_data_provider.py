"""
Live Market Data Provider

Uses yfinance to fetch live market data.
Supports NSE stocks (suffix .NS) and other exchanges.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data.contracts.market_data_provider import (
    MarketDataProvider,
)


class LiveMarketDataProvider(MarketDataProvider):
    """
    Version 1 Live Market Data Provider.

    Fetches OHLCV data using yfinance for live
    or recent market analysis.
    """

    def __init__(
        self,
        cache_dir: str | Path | None = None,
    ):
        self._cache_dir = (
            Path(cache_dir) if cache_dir else None
        )

    # ==========================================================
    # Metadata
    # ==========================================================

    @property
    def provider_name(self) -> str:
        return "LiveMarketDataProvider"

    @property
    def provider_type(self) -> str:
        return "API"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Historical Data
    # ==========================================================

    def load_historical_data(
        self,
        symbol: str | None = None,
        timeframe: str | None = None,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        import yfinance as yf

        if symbol is None:
            raise ValueError("Symbol is required.")

        period = self._determine_period(start_date, end_date)
        interval = self._map_timeframe(timeframe)

        ticker = yf.Ticker(symbol)
        df = ticker.history(
            period=period,
            interval=interval,
        )

        if df.empty:
            raise ValueError(
                f"No data returned for {symbol} "
                f"with period={period}, interval={interval}"
            )

        df = df.reset_index()
        df = self._normalize_columns(df)

        if start_date is not None:
            df = df[df["timestamp"] >= pd.Timestamp(start_date)]

        if end_date is not None:
            df = df[df["timestamp"] <= pd.Timestamp(end_date)]

        return df.reset_index(drop=True)

    # ==========================================================
    # Latest Data
    # ==========================================================

    def load_latest_data(
        self,
        symbol: str,
        timeframe: str,
        lookback: int = 500,
    ) -> pd.DataFrame:
        import yfinance as yf

        interval = self._map_timeframe(timeframe)
        period = self._lookback_to_period(lookback, interval)

        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            raise ValueError(
                f"No data returned for {symbol} "
                f"with period={period}, interval={interval}"
            )

        df = df.reset_index()
        df = self._normalize_columns(df)

        return df.tail(lookback).reset_index(drop=True)

    # ==========================================================
    # Helpers
    # ==========================================================

    def _normalize_columns(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        rename_map = {
            "Datetime": "timestamp",
            "Date": "timestamp",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
        df = df.rename(
            columns={
                col: new_col
                for col, new_col in rename_map.items()
                if col in df.columns
            }
        )

        for col in ["timestamp", "open", "high", "low", "close", "volume"]:
            if col not in df.columns:
                df[col] = None

        return df

    def _map_timeframe(
        self,
        timeframe: str | None,
    ) -> str:
        mapping = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "60m",
            "1d": "1d",
            "1w": "1wk",
            "1mo": "1mo",
        }
        if timeframe is None or timeframe not in mapping:
            return "1d"
        return mapping[timeframe]

    def _determine_period(
        self,
        start_date,
        end_date,
    ) -> str:
        if start_date is not None and end_date is not None:
            days = (
                pd.Timestamp(end_date)
                - pd.Timestamp(start_date)
            ).days
            if days <= 7:
                return "7d"
            if days <= 30:
                return "1mo"
            if days <= 90:
                return "3mo"
            if days <= 180:
                return "6mo"
            if days <= 365:
                return "1y"
            return "2y"
        return "1mo"

    def _lookback_to_period(
        self,
        lookback: int,
        interval: str,
    ) -> str:
        if interval in ("1m", "2m", "5m"):
            return "7d"
        if interval in ("15m", "30m"):
            return "1mo"
        if interval in ("60m", "90m"):
            return "3mo"
        if lookback >= 1000:
            return "5y"
        if lookback >= 500:
            return "2y"
        if lookback >= 250:
            return "1y"
        return "6mo"