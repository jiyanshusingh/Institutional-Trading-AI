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

    configuration = engine.analyze(df)

    print()

    print("======================")
    print("MARKET CONFIGURATION")
    print("======================")

    print("Events      :", len(configuration.structure_events))
    print("Segments    :", len(configuration.segments))
    print("Expansions  :", len(configuration.expansions))

    print()

    print("Latest Expansion")
    print("----------------")
    print(configuration.latest_expansion())
    
    print()

    print("Governing Expansion")
    print("-------------------")
    print(configuration.governing_expansion())

    print()

    print("===================")
    print("ALL EXPANSIONS")
    print("===================")
    
    print()

    print("Latest Structure Event")
    print("----------------------")
    print(configuration.latest_structure_event())

    for expansion in configuration.expansions:
        print(expansion)


if __name__ == "__main__":
    main()