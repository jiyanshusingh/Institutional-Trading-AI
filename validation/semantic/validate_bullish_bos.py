from pathlib import Path
from statistics import mean

from data.csv.csv_market_data_provider import CSVMarketDataProvider
from data.builders.observation_history_builder import (
    ObservationHistoryBuilder,
)

from domain.ontology.builders.swing_builder import SwingBuilder
from domain.ontology.builders.structure_event_builder import (
    StructureEventBuilder,
)

from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)

from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)

from domain.ontology.candidates.ict.ict_structure_event_candidate_detector import (
    ICTStructureEventCandidateDetector,
)

from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)

from domain.ontology.policies.ict.ict_structure_event_confirmation_policy import (
    ICTStructureEventConfirmationPolicy,
)

from domain.ontology.structure_event import (
    StructureDirection,
    StructureEventType,
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

    structure_builder = StructureEventBuilder(
        detector=ICTStructureEventCandidateDetector(),
        confirmation_policy=ICTStructureEventConfirmationPolicy(),
    )

    events = structure_builder.build(
        observation_history=history,
        swings=swings,
    )

    bullish_bos = [
        e
        for e in events
        if (
            e.event_type == StructureEventType.BOS
            and
            e.direction == StructureDirection.BULLISH
        )
    ]

    print("=" * 70)
    print("BULLISH BOS VALIDATION")
    print("=" * 70)

    print(f"Observations : {len(history)}")
    print(f"Swings       : {len(swings)}")
    print(f"BOS Events   : {len(bullish_bos)}")

    high_swings = sum(s.is_high for s in swings)
    low_swings = sum(s.is_low for s in swings)

    print()
    print("Swing Statistics")
    print("-" * 70)

    print(f"High Swings  : {high_swings}")
    print(f"Low Swings   : {low_swings}")

    if high_swings:

        ratio = len(bullish_bos) / high_swings

        print(f"BOS Ratio    : {ratio:.2%}")

    if bullish_bos:

        displacements = [
            e.displacement
            for e in bullish_bos
        ]

        print()
        print("Displacement Statistics")
        print("-" * 70)

        print(f"Minimum : {min(displacements):.4f}")
        print(f"Average : {mean(displacements):.4f}")
        print(f"Maximum : {max(displacements):.4f}")

    print()
    print("First 10 BOS")
    print("-" * 70)

    for event in bullish_bos[:10]:

        print(
            f"Candle={event.candle_index:<8}"
            f"Swing={event.broken_swing_index:<8}"
            f"Price={event.price:<10.2f}"
            f"Disp={event.displacement:<8.2f}"
        )

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()