from pathlib import Path

import pandas as pd
import pytest

from data.csv.csv_market_data_provider import (
    CSVMarketDataProvider,
)


# ==========================================================
# Helpers
# ==========================================================

def create_csv(tmp_path: Path) -> Path:

    df = pd.DataFrame(
        {
            "timestamp": [
                "2025-01-01 09:15:00",
                "2025-01-01 09:30:00",
                "2025-01-01 09:45:00",
            ],
            "open": [100, 102, 104],
            "high": [103, 105, 106],
            "low": [99, 101, 103],
            "close": [102, 104, 105],
            "volume": [1000, 1200, 1400],
        }
    )

    csv_path = tmp_path / "sample.csv"

    df.to_csv(csv_path, index=False)

    return csv_path


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    provider = CSVMarketDataProvider(
        "dummy.csv"
    )

    assert (
        provider.provider_name
        == "CSVMarketDataProvider"
    )

    assert provider.provider_type == "CSV"

    assert provider.version == "1.0"


# ==========================================================
# Historical Data
# ==========================================================

def test_load_historical_data(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data()

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 3


def test_required_columns_exist(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data()

    assert tuple(df.columns) == (
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    )


def test_timestamp_is_datetime(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data()

    assert pd.api.types.is_datetime64_any_dtype(
        df["timestamp"]
    )


# ==========================================================
# Latest Data
# ==========================================================

def test_load_latest_data(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_latest_data(
        symbol="RELIANCE",
        timeframe="15m",
        lookback=2,
    )

    assert len(df) == 2

    assert df.iloc[-1]["close"] == 105


# ==========================================================
# Validation
# ==========================================================

def test_missing_csv():

    provider = CSVMarketDataProvider(
        "does_not_exist.csv"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        provider.load_historical_data()


def test_missing_required_column(tmp_path):

    df = pd.DataFrame(
        {
            "timestamp": [
                "2025-01-01"
            ],
            "open": [100],
            "high": [101],
            "low": [99],
            "close": [100],
            # volume intentionally omitted
        }
    )

    csv_path = (
        tmp_path / "invalid.csv"
    )

    df.to_csv(csv_path, index=False)

    provider = CSVMarketDataProvider(
        csv_path
    )

    with pytest.raises(
        ValueError
    ):
        provider.load_historical_data()


# ==========================================================
# Date Filtering
# ==========================================================

def test_start_date_filter(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data(
        start_date="2025-01-01 09:30:00"
    )

    assert len(df) == 2


def test_end_date_filter(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data(
        end_date="2025-01-01 09:30:00"
    )

    assert len(df) == 2


def test_date_range_filter(tmp_path):

    csv_path = create_csv(tmp_path)

    provider = CSVMarketDataProvider(
        csv_path
    )

    df = provider.load_historical_data(
        start_date="2025-01-01 09:30:00",
        end_date="2025-01-01 09:30:00",
    )

    assert len(df) == 1

    assert (
        df.iloc[0]["close"]
        == 104
    )