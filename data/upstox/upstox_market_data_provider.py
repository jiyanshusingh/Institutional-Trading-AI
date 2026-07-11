from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import pandas as pd

from data.contracts.market_data_provider import MarketDataProvider


_UPSTOX_BASE = "https://api.upstox.com/v2"


class UpstoxMarketDataProvider(MarketDataProvider):
    def __init__(
        self,
        access_token: str,
        cache_dir: str | Path | None = None,
    ):
        self._access_token = access_token
        self._cache_dir = Path(cache_dir) if cache_dir else None
        self._session = None

    @property
    def provider_name(self) -> str:
        return "UpstoxMarketDataProvider"

    @property
    def provider_type(self) -> str:
        return "API"

    @property
    def version(self) -> str:
        return "1.0"

    # ── Session ──────────────────────────────────────────────────

    def _get_session(self):
        if self._session is None:
            import requests
            self._session = requests.Session()
            self._session.headers.update({
                "Authorization": f"Bearer {self._access_token}",
                "Accept": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            })
        return self._session

    # ── Historical Data ──────────────────────────────────────────

    def load_historical_data(
        self,
        symbol: str | None = None,
        timeframe: str | None = None,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        if symbol is None:
            raise ValueError("Symbol (instrument key) is required.")

        interval = self._map_timeframe(timeframe)
        to_date = self._fmt_date(end_date or datetime.now())
        from_date = self._fmt_date(start_date or (datetime.now() - timedelta(days=30)))

        df = self._fetch_candles(symbol, interval, to_date, from_date)

        tz = df["timestamp"].dt.tz
        if start_date is not None:
            sd = pd.Timestamp(start_date)
            if tz is not None and sd.tzinfo is None:
                sd = sd.tz_localize(tz)
            df = df[df["timestamp"] >= sd]
        if end_date is not None:
            ed = pd.Timestamp(end_date)
            if tz is not None and ed.tzinfo is None:
                ed = ed.tz_localize(tz)
            df = df[df["timestamp"] <= ed]

        return df.reset_index(drop=True)

    def load_latest_data(
        self,
        symbol: str,
        timeframe: str,
        lookback: int = 500,
    ) -> pd.DataFrame:
        interval = self._map_timeframe(timeframe)
        days = self._lookback_to_days(lookback, interval)
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)

        df = self._fetch_candles(symbol, interval, self._fmt_date(to_date), self._fmt_date(from_date))

        return df.tail(lookback).reset_index(drop=True)

    # ── API Call ──────────────────────────────────────────────────

    def _fetch_candles(
        self,
        instrument_key: str,
        interval: str,
        to_date: str,
        from_date: str,
    ) -> pd.DataFrame:
        session = self._get_session()
        encoded = quote(instrument_key, safe="")
        url = (
            f"{_UPSTOX_BASE}/historical-candle/"
            f"{encoded}/{interval}/{to_date}/{from_date}"
        )

        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Upstox API error {resp.status_code} for {instrument_key}: {resp.text[:200]}"
            )

        body = resp.json()
        candles = body.get("data", {}).get("candles", [])
        if not candles:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

        df = pd.DataFrame(
            candles,
            columns=["timestamp", "open", "high", "low", "close", "volume", "open_interest"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)
        df = df.drop(columns=["open_interest"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        return df

    # ── Helpers ──────────────────────────────────────────────────

    def _map_timeframe(self, timeframe: str | None) -> str:
        mapping = {
            "1m": "1minute",
            "5m": "1minute",
            "15m": "30minute",
            "30m": "30minute",
            "1h": "30minute",
            "1d": "day",
            "1w": "week",
            "1mo": "month",
        }
        if timeframe is None or timeframe not in mapping:
            return "day"
        return mapping[timeframe]

    @staticmethod
    def _fmt_date(dt) -> str:
        if isinstance(dt, str):
            return dt[:10]
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def _lookback_to_days(lookback: int, interval: str) -> int:
        multipliers = {
            "1minute": 0.7,
            "30minute": 20,
            "day": 400,
            "week": 2000,
            "month": 8000,
        }
        mult = multipliers.get(interval, 30)
        return max(mult, int(lookback * mult / 400) + 1)

    @property
    def supported_timeframes(self) -> list[str]:
        return ["1m", "15m", "1h", "1d"]
