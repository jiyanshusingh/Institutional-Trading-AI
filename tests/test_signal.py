from engines.data_engine import DataEngine
from engines.indicator_engine import IndicatorEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fvg_engine import FVGEngine
from engines.liquidity_engine import LiquidityEngine
from engines.premium_discount_engine import PremiumDiscountEngine
from engines.signal_engine import SignalEngine


engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

indicator = IndicatorEngine()
df = indicator.calculate(df)

market = MarketStructure(df)
df = market.detect_swings()
df = market.classify_structure()
df = market.detect_bos()

smc = SMCEngine(df)
df = smc.detect_choch()

ob = OrderBlockEngine(df)
df = ob.detect_order_blocks()

fvg = FVGEngine(df)
df = fvg.detect_fvg()

liq = LiquidityEngine(df)
df = liq.detect_liquidity_sweeps()

premium = PremiumDiscountEngine(df)
df = premium.detect_zones()

signal = SignalEngine(df)

result = signal.generate_signal()

print(result)