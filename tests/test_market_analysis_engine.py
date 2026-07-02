from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine


def main():

    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    engine = MarketAnalysisEngine()

    expansions = engine.analyze(df)

    print()

    print("===================")
    print("EXPANSIONS")
    print("===================")

    for expansion in expansions:
        print(expansion)


if __name__ == "__main__":
    main()