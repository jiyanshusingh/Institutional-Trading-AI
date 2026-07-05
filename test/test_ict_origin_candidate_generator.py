from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine
from policies.origin_region.ict.ict_origin_candidate_generator import (
    ICTOriginCandidateGenerator
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
    # Build Configuration
    # ----------------------------------

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    # ----------------------------------
    # Latest Expansion
    # ----------------------------------

    expansion = configuration.latest_expansion()

    if expansion is None:
        print("No Expansion Found")
        return

    # ----------------------------------
    # Candidate Generation
    # ----------------------------------

    generator = ICTOriginCandidateGenerator()

    candidates = generator.generate(
        expansion,
        configuration
    )

    # ----------------------------------
    # Output
    # ----------------------------------

    print()
    print("===========================")
    print("ORIGIN CANDIDATES")
    print("===========================")

    print("Expansion")
    print(expansion)

    print()
    print("Candidates:", len(candidates))
    print()

    for candidate in candidates:
        print(candidate)


if __name__ == "__main__":
    main()