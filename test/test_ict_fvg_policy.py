from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

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

    policy = ICTFairValueGapPolicy()

    fvgs = policy.detect(configuration)

    print()

    print("===================")
    print("ICT FVG POLICY")
    print("===================")

    print()

    print("FVGs :", len(fvgs))

    print()

    for fvg in fvgs:
        print(fvg)


if __name__ == "__main__":
    main()