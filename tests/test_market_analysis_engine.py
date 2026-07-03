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

    print("Events          :", len(configuration.structure_events))
    print("Segments        :", len(configuration.segments))
    print("Expansions      :", len(configuration.expansions))
    print("Origin Regions  :", len(configuration.origin_regions))

    print()

    print("Latest Structure Event")
    print("----------------------")
    print(configuration.latest_structure_event())

    print()

    print("Latest Expansion")
    print("----------------")
    print(configuration.latest_expansion())

    print()

    print("Governing Expansion")
    print("-------------------")
    print(configuration.governing_expansion())

    print()

    print("Latest Origin Region")
    print("--------------------")

    if configuration.origin_regions:
        print(configuration.origin_regions[-1])
    else:
        print("None")

    print()

    print("===================")
    print("ALL EXPANSIONS")
    print("===================")

    for expansion in configuration.expansions:
        print(expansion)

    print()

    print("======================")
    print("ALL ORIGIN REGIONS")
    print("======================")

    for region in configuration.origin_regions:
        print(region)
        
    print()
    print("Order Blocks")
    print("------------")
    print(len(configuration.order_blocks))

    print()

    for order_block in configuration.order_blocks:
        print(order_block)
    
    print()
    print("Fair Value Gaps")
    print("----------------")
    print(len(configuration.fair_value_gaps))
    
    print()
    print("Latest Fair Value Gap")
    print("---------------------")
    print(configuration.latest_fair_value_gap())
    
    print()
    print("======================")
    print("ALL FAIR VALUE GAPS")
    print("======================")
    for fvg in configuration.fair_value_gaps:
        print(fvg)

if __name__ == "__main__":
    main()