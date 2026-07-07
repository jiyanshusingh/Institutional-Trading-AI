from pathlib import Path

import pandas as pd

from data.csv.csv_market_data_provider import CSVMarketDataProvider
from data.builders.observation_history_builder import (
    ObservationHistoryBuilder,
)

from domain.ontology.builders.swing_builder import SwingBuilder
from domain.ontology.candidates.ict.ict_swing_candidate_detector import (
    ICTSwingCandidateDetector,
)
from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)
from domain.ontology.policies.ict.ict_swing_confirmation_policy import (
    ICTSwingConfirmationPolicy,
)
from domain.ontology.swing_type import SwingType


INPUT_CSV = Path(
    "historical_data/normalized/ACUTAAS_1m.csv"
)

OUTPUT_CSV = Path(
    "validation/output/broken_swings.csv"
)


def find_break(
    history,
    swing,
):
    """
    Returns information about the first candle
    that breaks the swing.

    Returns
    -------
    tuple:
        (
            broken,
            break_index,
            break_timestamp,
            break_price,
            break_high,
            break_low,
            break_close,
        )
    """

    observations = history.observations

    start = swing.confirmation_index + 1

    for i in range(start, len(observations)):

        candle = observations[i]

        if swing.swing_type == SwingType.HIGH:

            if candle.high > swing.price:

                return (
                    True,
                    i,
                    candle.timestamp,
                    candle.high,
                    candle.high,
                    candle.low,
                    candle.close,
                )

        else:

            if candle.low < swing.price:

                return (
                    True,
                    i,
                    candle.timestamp,
                    candle.low,
                    candle.high,
                    candle.low,
                    candle.close,
                )

    return (
        False,
        None,
        None,
        None,
        None,
        None,
        None,
    )

def previous_same_type_swing_id(
    swings,
    current_position,
):
    """
    Returns the immediately previous swing of the
    same type.
    """

    current = swings[current_position]

    for i in range(current_position - 1, -1, -1):

        if swings[i].swing_type == current.swing_type:
            return i + 1

    return None


def latest_same_type_swing_id(
    swings,
    current_position,
    break_index,
):
    """
    Returns the latest confirmed swing of the same
    type that existed before the break candle.

    If none exists, returns the current swing.
    """

    current = swings[current_position]

    latest = current_position

    for i in range(current_position + 1, len(swings)):

        swing = swings[i]

        if swing.confirmation_index >= break_index:
            break

        if swing.swing_type == current.swing_type:
            latest = i

    return latest + 1


def count_swings_before_break(
    swings,
    current_position,
    break_index,
):
    """
    Counts confirmed swings between the current
    swing confirmation and the break candle.
    """

    current = swings[current_position]

    same = 0
    opposite = 0

    for i in range(current_position + 1, len(swings)):

        swing = swings[i]

        if swing.confirmation_index >= break_index:
            break

        if swing.swing_type == current.swing_type:
            same += 1
        else:
            opposite += 1

    return (
        same,
        opposite,
    )
def main():

    provider = CSVMarketDataProvider(INPUT_CSV)

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

    rows = []

    for swing_id, swing in enumerate(swings, start=1):

        (
            broken,
            break_index,
            break_timestamp,
            break_price,
            break_high,
            break_low,
            break_close,
        ) = find_break(
            history,
            swing,
        )

        if not broken:
            continue
        previous_same = previous_same_type_swing_id(
            swings,
            swing_id - 1,
        )

        latest_same =latest_same_type_swing_id(
            swings,
            swing_id - 1,
            break_index,
        )

        (
            same_before_break,
            opposite_before_break,
        ) = count_swings_before_break(
            swings,
            swing_id - 1,
            break_index,
        )

        superseded = latest_same != swing_id
        rows.append(
            {
                "Swing_ID": swing_id,
                "Swing_Type": swing.swing_type.value,
                "Swing_Index": swing.index,
                "Confirmation_Index": swing.confirmation_index,
                "Swing_Timestamp": swing.timestamp,
                "Swing_Price": swing.price,
                "Broken": broken,
                "Break_Index": break_index,
                "Break_Timestamp": break_timestamp,
                "Break_Price": break_price,
                "Break_High": break_high,
                "Break_Low": break_low,
                "Break_Close": break_close,
                "Candles_To_Break": (
                    break_index - swing.confirmation_index
                ),
                "Previous_Same_Type_Swing_ID":
                previous_same,

                "Latest_Same_Type_Swing_ID":
                latest_same,

                "Same_Type_Swings_Before_Break":
                same_before_break,

                "Opposite_Type_Swings_Before_Break":
                opposite_before_break,

                "Superseded_By_Same_Type":
                superseded,
            }
        )

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = pd.DataFrame(rows)

    result.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print("=" * 60)
    print("BROKEN SWING EXPORT")
    print("=" * 60)
    print(f"Total Swings   : {len(swings)}")
    print(f"Broken Swings  : {len(result)}")
    print(f"Output         : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()