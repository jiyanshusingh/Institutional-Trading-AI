from engines.data_engine import DataEngine
from engines.indicator_engine import IndicatorEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine
from engines.liquidity_engine import LiquidityEngine
from engines.premium_discount_engine import PremiumDiscountEngine
from engines.order_block_engine import OrderBlockEngine
from engines.fvg_engine import FVGEngine
from engines.signal_engine import SignalEngine
from engines.risk_engine import RiskEngine


def analyze_stock(symbol):

    engine = DataEngine()

    df = engine.get_data(
        symbol,
        period="1y",
        interval="1d"
    )

    # Indicators
    ind = IndicatorEngine()
    df = ind.calculate(df)

    # Market Structure
    ms = MarketStructure(df)
    df = ms.detect_swings()
    df = ms.classify_structure()
    df = ms.detect_bos()

    # SMC
    smc = SMCEngine(df)
    df = smc.detect_choch()

    # Liquidity
    liq = LiquidityEngine(df)
    df =liq.detect_liquidity_sweeps()
    
    # Premium / Discount
    pd_engine = PremiumDiscountEngine(df)
    df = pd_engine.detect_zones()

    # Order Blocks
    ob = OrderBlockEngine(df)
    df = ob.detect_order_blocks()

    # Fair Value Gaps
    fvg = FVGEngine(df)
    df = fvg.detect_fvg()

    # Signal
    signal = SignalEngine(df)
    result = signal.generate_signal()

    # Risk
    risk = RiskEngine(df)
    trade = risk.calculate()

    return {
        "symbol": symbol,
        "df": df,
        "signal": result,
        "risk": trade
    }