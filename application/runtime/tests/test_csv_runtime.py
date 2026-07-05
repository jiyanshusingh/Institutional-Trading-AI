from pathlib import Path

import pandas as pd

from application.runtime.csv_runtime import CSVRuntime
from application.pipeline.pipeline_result import PipelineResult


# ==========================================================
# Test Doubles
# ==========================================================

class DummyTradingPipeline:

    def run(self, market):

        return PipelineResult(
            pipeline_id="PIPELINE-001",
            created_at=pd.Timestamp.now(),

            market=market,

            market_theses=(),

            opportunities=(),

            opportunity_assessments=(),

            opportunity_rankings=(),

            portfolio_decision=None,

            trade_candidates=(),

            execution_plans=(),
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

    path = tmp_path / "sample.csv"

    df.to_csv(path, index=False)

    return path


# ==========================================================
# Runtime
# ==========================================================

def test_csv_runtime_returns_pipeline_result(
    tmp_path,
):

    runtime = CSVRuntime(
        DummyTradingPipeline()
    )

    csv_path = create_csv(
        tmp_path
    )

    result = runtime.run(
        csv_path=csv_path,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert isinstance(
        result,
        PipelineResult,
    )


def test_symbol_propagates(
    tmp_path,
):

    runtime = CSVRuntime(
        DummyTradingPipeline()
    )

    csv_path = create_csv(
        tmp_path
    )

    result = runtime.run(
        csv_path=csv_path,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert result.market.symbol == "RELIANCE"


def test_timeframe_propagates(
    tmp_path,
):

    runtime = CSVRuntime(
        DummyTradingPipeline()
    )

    csv_path = create_csv(
        tmp_path
    )

    result = runtime.run(
        csv_path=csv_path,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert result.market.timeframe == "15m"


def test_observation_count(
    tmp_path,
):

    runtime = CSVRuntime(
        DummyTradingPipeline()
    )

    csv_path = create_csv(
        tmp_path
    )

    result = runtime.run(
        csv_path=csv_path,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert (
        result.market.observation_count
        == 3
    )


def test_runtime_builds_market_model(
    tmp_path,
):

    runtime = CSVRuntime(
        DummyTradingPipeline()
    )

    csv_path = create_csv(
        tmp_path
    )

    result = runtime.run(
        csv_path=csv_path,
        symbol="RELIANCE",
        timeframe="15m",
    )

    assert result.market is not None

    assert (
        result.market.summary
        is not None
    )