from __future__ import annotations

from pathlib import Path

from application.pipeline.trading_pipeline import (
    TradingPipeline,
)

from application.pipeline.pipeline_result import (
    PipelineResult,
)

from data.csv.csv_market_data_provider import (
    CSVMarketDataProvider,
)

from data.builders.observation_history_builder import (
    ObservationHistoryBuilder,
)

from domain.semantic_construction.semantic_construction_pipeline import (
    SemanticConstructionPipeline,
)


class CSVRuntime:
    """
    Version 1 CSV Runtime.

    Executes the complete Institutional Trading AI
    pipeline from a historical CSV file.

    Pipeline

    CSV
        ↓
    DataFrame
        ↓
    ObservationHistory
        ↓
    CanonicalMarketModel
        ↓
    TradingPipeline
        ↓
    PipelineResult
    """

    def __init__(
        self,
        trading_pipeline: TradingPipeline,
    ):

        self._provider_builder = (
            ObservationHistoryBuilder()
        )

        self._semantic_pipeline = (
            SemanticConstructionPipeline()
        )

        self._trading_pipeline = (
            trading_pipeline
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        csv_path: str | Path,
        symbol: str,
        timeframe: str,
    ) -> PipelineResult:
        """
        Execute the complete runtime.

        Parameters
        ----------
        csv_path
            Historical CSV file.

        symbol
            Trading symbol.

        timeframe
            Candle timeframe.

        Returns
        -------
        PipelineResult
        """

        provider = CSVMarketDataProvider(
            csv_path
        )

        dataframe = (
            provider.load_historical_data()
        )

        observation_history = (
            self._provider_builder.build(
                df=dataframe,
                symbol=symbol,
                timeframe=timeframe,
                source="CSV",
            )
        )

        market = (
            self._semantic_pipeline.build(
                observation_history
            )
        )

        return self._trading_pipeline.run(
            market
        )