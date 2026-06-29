from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fvg_engine import FVGEngine


engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

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

print(
    df[
        [
            "High",
            "Low",
            "Bullish_FVG",
            "Bearish_FVG",
            "FVG_High",
            "FVG_Low",
        ]
    ].tail(80)
)