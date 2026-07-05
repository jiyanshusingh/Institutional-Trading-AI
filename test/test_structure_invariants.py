from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.structure_event_engine import StructureEventEngine

SYMBOL = "TRENT.NS"


def run(symbol):

    print("\n" + "=" * 70)
    print(f"VALIDATING : {symbol}")
    print("=" * 70)

    engine = DataEngine()

    df = engine.get_data(
        symbol,
        period="1y",
        interval="1d"
    )

    ms = MarketStructure(df)

    df = ms.detect_swings()
    df = ms.classify_structure()
    df = ms.detect_trend_candidate()
    df = ms.detect_protected_swings()
    df = ms.detect_bos()
    df = ms.detect_choch()
    df = ms.detect_market_state()

    event_engine = StructureEventEngine(df)

    events = event_engine.generate_events()

    if len(events) == 0:
        print("No BOS Events Found")
        return

    print()

    for event in events:

        base_index = event["base_swing_index"]
        broken_index = event["broken_swing_index"]
        bos_index = event["candle_index"]

        structure_rows = df[
            (
                df["Structure"].notna()
            ) |
            (
                df["Bullish_BOS"]
            ) |
            (
                df["Bearish_BOS"]
            )
        ]
        print(
            df["Structure"]
            .value_counts(dropna=False)
        )

        print(
            structure_rows[
                [
                    "Structure",
                    "Protected_High",
                    "Protected_Low",
                    "Bearish_BOS",
                    "Bullish_BOS"
                ]
            ].head(40)
        )

run(SYMBOL)