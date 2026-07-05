from datetime import datetime

import pandas as pd
import pytest

from data.builders.observation_history_builder import (
    ObservationHistoryBuilder,
)
from domain.market_observation.observation_history import (
    ObservationHistory,
)


# ==========================================================
# Helpers
# ==========================================================

def make_dataframe() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "timestamp": [
                datetime(2025, 1, 1, 9, 15),
                datetime(2025, 1, 1, 9, 30),
                datetime(2025, 1, 1, 9, 45),
            ],
            "open": [100.0, 102.0, 104.0],
            "high": [103.0, 105.0, 106.0],
            "low": [99.0, 101.0, 103.0],
            "close": [102.0, 104.0, 105.0],
            "volume": [1000, 1200, 1500],
        }
    )


# ==========================================================
# Creation
# ==========================================================

def test_build_returns_observation_history():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert isinstance(
        history,
        ObservationHistory,
    )


def test_observation_count():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert len(history) == 3


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    metadata = history.metadata

    assert metadata.symbol == "RELIANCE"

    assert metadata.timeframe == "15m"

    assert metadata.observation_count == 3

    assert metadata.source == "CSV"


def test_start_and_end_time():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert (
        history.metadata.start_time
        == datetime(2025, 1, 1, 9, 15)
    )

    assert (
        history.metadata.end_time
        == datetime(2025, 1, 1, 9, 45)
    )


# ==========================================================
# Observations
# ==========================================================

def test_first_observation():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    first = history.first

    assert first.open == 100.0
    assert first.high == 103.0
    assert first.low == 99.0
    assert first.close == 102.0


def test_last_observation():

    builder = ObservationHistoryBuilder()

    history = builder.build(
        df=make_dataframe(),
        symbol="RELIANCE",
        timeframe="15m",
    )

    last = history.last

    assert last.open == 104.0
    assert last.high == 106.0
    assert last.low == 103.0
    assert last.close == 105.0


# ==========================================================
# Validation
# ==========================================================

def test_empty_dataframe():

    builder = ObservationHistoryBuilder()

    df = pd.DataFrame(
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    )

    with pytest.raises(
        ValueError,
        match="DataFrame cannot be empty.",
    ):

        builder.build(
            df=df,
            symbol="RELIANCE",
            timeframe="15m",
        )


def test_missing_column():

    builder = ObservationHistoryBuilder()

    df = make_dataframe().drop(
        columns=["volume"]
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):

        builder.build(
            df=df,
            symbol="RELIANCE",
            timeframe="15m",
        )


# ==========================================================
# Sorting
# ==========================================================

def test_unsorted_dataframe_is_sorted():

    builder = ObservationHistoryBuilder()

    df = make_dataframe().iloc[::-1]

    history = builder.build(
        df=df,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert (
        history.first.timestamp
        < history.last.timestamp
    )


# ==========================================================
# Missing Volume
# ==========================================================

def test_missing_volume_becomes_none():

    builder = ObservationHistoryBuilder()

    df = make_dataframe()

    df.loc[1, "volume"] = None

    history = builder.build(
        df=df,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert (
        history[1].volume
        is None
    )