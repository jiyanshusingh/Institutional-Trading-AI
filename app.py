from engines.data_engine import DataEngine
from engines.indicator_engine import IndicatorEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fvg_engine import FVGEngine
from engines.liquidity_engine import LiquidityEngine
from engines.premium_discount_engine import PremiumDiscountEngine


def main():

    print("=" * 60)
    print("🏦 Institutional Trading AI")
    print("=" * 60)

    symbol = input("Enter NSE Symbol: ").strip().upper()

    engine = DataEngine()

    df = engine.get_data(symbol)

    indicator = IndicatorEngine()
    df = indicator.calculate(df)

    market = MarketStructure(df)
    df = market.detect_swings()
    df = market.classify_structure()
    df = market.detect_bos()

    smc = SMCEngine(df)
    df = smc.detect_choch()

    order_block = OrderBlockEngine(df)
    df = order_block.detect_order_blocks()

    fvg = FVGEngine(df)
    df = fvg.detect_fvg()

    liquidity = LiquidityEngine(df)
    df = liquidity.detect_liquidity_sweeps()

    premium = PremiumDiscountEngine(df)
    df = premium.detect_zones()

    print("\nAnalysis Complete!\n")
    print(df.tail())


if __name__ == "__main__":
    main()