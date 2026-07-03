from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from engines.fair_value_gap_engine import (
    FairValueGapEngine
)

from policies.fair_value_gap.ict.ict_fvg_policy import (
    ICTFairValueGapPolicy
)


def main():

    data = DataEngine()

    df = data.get_data(

        "RELIANCE.NS",

        period="1y",

        interval="1d"

    )

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    fvg_engine = FairValueGapEngine(

        configuration=configuration,

        policy=ICTFairValueGapPolicy()

    )

    fvgs = fvg_engine.build()

    print()

    print("==========================")
    print("FAIR VALUE GAP ENGINE")
    print("==========================")

    print()

    print("FVGs :", len(fvgs))

    print()

    for fvg in fvgs:

        print(fvg)


if __name__ == "__main__":
    main()