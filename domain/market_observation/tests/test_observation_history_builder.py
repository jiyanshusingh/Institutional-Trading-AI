import pandas as pd

from domain.market_observation.observation_history_builder import (
    ObservationHistoryBuilder,
)


def test_builder_from_dataframe():

    df = pd.DataFrame(
        {
            "Datetime": [
                "2026-01-01 09:15",
                "2026-01-01 09:30",
            ],
            "Open": [100, 103],
            "High": [105, 106],
            "Low": [99, 102],
            "Close": [103, 105],
            "Volume": [100, 120],
        }
    )

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    history = ObservationHistoryBuilder.from_dataframe(
        df=df,
        symbol="MARICO.NS",
        timeframe="15m",
    )

    assert len(history) == 2
    assert history.metadata.symbol == "MARICO.NS"
    assert history.metadata.timeframe == "15m"
    assert history.first.open == 100
    assert history.last.close == 105