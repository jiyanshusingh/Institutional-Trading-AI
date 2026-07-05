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

    events = structure_builder.build(history)

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

    for event in events[:10]:
        print(event)


if __name__ == "__main__":
    main()