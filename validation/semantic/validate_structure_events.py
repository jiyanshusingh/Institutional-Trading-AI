from pathlib import Path

from data.csv.csv_market_data_provider import CSVMarketDataProvider
from data.builders.observation_history_builder import (
    ObservationHistoryBuilder,
)

from domain.ontology.builders.swing_builder import SwingBuilder
from domain.ontology.builders.structure_event_builder import (
    StructureEventBuilder,
)

from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)
from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)
from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)

from domain.ontology.candidates.ict.ict_structure_event_candidate_detector import (
    ICTStructureEventCandidateDetector,
)
from domain.ontology.policies.ict.ict_structure_event_confirmation_policy import (
    ICTStructureEventConfirmationPolicy,
)


def main():

    provider = CSVMarketDataProvider(
        Path("historical_data/normalized/ACUTAAS_1m.csv")
    )

    df = provider.load_historical_data()

    history = ObservationHistoryBuilder().build(
        df=df,
        symbol="ACUTAAS",
        timeframe="1m",
    )

    swing_builder = SwingBuilder(
        detector=ICTSwingCandidateDetector(
            lookback=1,
        ),
        confirmation_policy=ICTSwingConfirmationPolicy(
            strength_calculator=SwingStrengthCalculator(),
            lookback=1,
        ),
    )

    swings = swing_builder.build(history)

    print("=" * 60)
    print("SWINGS")
    print("=" * 60)
    print("Count:", len(swings))

    structure_builder = StructureEventBuilder(
        detector=ICTStructureEventCandidateDetector(),
        confirmation_policy=ICTStructureEventConfirmationPolicy(),
    )

    events = structure_builder.build(
        observation_history=history,
        swings=swings,
    )
    print()
    print("=" * 60)
    print("STRUCTURE EVENTS")
    print("=" * 60)
    print("Count:", len(events))

    print()
    print("First 10 Swings")
    print("-" * 60)

    for swing in swings[:10]:
        print(swing)

    print()
    print("First 10 Structure Events")
    print("-" * 60)
    
    print()
    print("First 10 Bullish BOS")

    for event in events[:10]:
        print(
            f"{event.event_type.name} | "
            f"{event.direction.name} | "
            f"Swing={event.broken_swing_index} | "
            f"Candle={event.candle_index} | "
            f"Price={event.price:.2f}"
        )

    for event in events[:10]:
        print(event)
        
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    high_swings = sum(1 for s in swings if s.is_high)
    low_swings = sum(1 for s in swings if s.is_low)

    print(f"High Swings : {high_swings}")
    print(f"Low Swings  : {low_swings}")
    print(f"BOS Events  : {len(events)}")


if __name__ == "__main__":
    main()