from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fvg_engine import FVGEngine
from engines.liquidity_engine import LiquidityEngine
from engines.premium_discount_engine import PremiumDiscountEngine

engine = DataEngine()

df = engine.get_data("MARICO.NS", period="1y", interval="1d")

ms = MarketStructure(df)
df = ms.detect_swings()
df = ms.classify_structure()
df = ms.detect_bos()

smc = SMCEngine(df)
df = smc.detect_choch()

ob = OrderBlockEngine(df)
df = ob.detect_order_blocks()

fvg = FVGEngine(df)
df = fvg.detect_fvg()

liq = LiquidityEngine(df)
df = liq.detect_liquidity_sweeps()

pdz = PremiumDiscountEngine(df)
df = pdz.detect_zones()

print(
    df[
        [
            "Close",
            "Equilibrium",
            "Premium_Zone",
            "Discount_Zone",
        ]
    ].tail(80)
)