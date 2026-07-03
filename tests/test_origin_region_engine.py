from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from engines.origin_region_engine import OriginRegionEngine

from policies.origin_region.ict_origin_region_policy import (
    ICTOriginRegionPolicy
)


def main():

    # ----------------------------------
    # Load Data
    # ----------------------------------

    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    # ----------------------------------
    # Build Market Configuration
    # ----------------------------------

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    # ----------------------------------
    # Build Origin Regions
    # ----------------------------------

    origin_engine = OriginRegionEngine(

        expansions=configuration.expansions,

        configuration=configuration,

        policy=ICTOriginRegionPolicy()

    )

    origin_regions = origin_engine.build()

    # ----------------------------------
    # Output
    # ----------------------------------

    print()

    print("===========================")
    print("ORIGIN REGION ENGINE")
    print("===========================")

    print()

    print("Expansions :", len(configuration.expansions))
    print("Regions    :", len(origin_regions))

    print()

    for region in origin_regions:
        print(region)


if __name__ == "__main__":
    main()