"""
Market Data Provider Contract

Version 1.0

A MarketDataProvider supplies historical or live market
data to the trading platform.

It abstracts the underlying data source.

Examples

- CSVMarketDataProvider
- ZerodhaMarketDataProvider
- UpstoxMarketDataProvider
- BinanceMarketDataProvider
- PolygonMarketDataProvider
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class MarketDataProvider(ABC):
    """
    Abstract Market Data Provider.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        ...

    @property
    @abstractmethod
    def provider_type(self) -> str:
        """
        Provider type.

        Examples
        --------
        CSV
        LIVE
        DATABASE
        API
        WEBSOCKET
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Provider version.
        """
        ...

    # ==========================================================
    # Historical Data
    # ==========================================================

    @abstractmethod
    def load_historical_data(
        self,
        symbol: str,
        timeframe: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        """
        Load historical OHLCV market data.

        Parameters
        ----------
        symbol
            Trading symbol.

        timeframe
            Candle timeframe.

        start_date
            Optional start date.

        end_date
            Optional end date.

        Returns
        -------
        pandas.DataFrame

        Required columns

        timestamp
        open
        high
        low
        close
        volume
        """
        ...

    # ==========================================================
    # Latest Market Data
    # ==========================================================

    @abstractmethod
    def load_latest_data(
        self,
        symbol: str,
        timeframe: str,
        lookback: int = 500,
    ) -> pd.DataFrame:
        """
        Load the latest candles.

        Parameters
        ----------
        symbol
            Trading symbol.

        timeframe
            Candle timeframe.

        lookback
            Number of candles to return.

        Returns
        -------
        pandas.DataFrame
        """
        ...