"""
Trading Strategy Registry

Machine-readable registry of all trading strategies/frameworks
used by traders, with metadata, requirements, and implementation status.

Each entry contains:
  - name, creator, category
  - core_concepts
  - data_requirements (what data/indicators are needed)
  - components_used (existing codebase modules that implement parts)
  - gaps (what's missing)
  - timeframes, asset_classes, holding_period
  - confidence: "IMPLEMENTED" | "PARTIAL" | "PLANNED" | "NOT_STARTED"
  - best_conditions: list of DayType values this works best in
  - stock_types: list of StockType values this works best with
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Strategy:
    name: str
    creator: str
    category: str
    description: str
    core_concepts: list[str]
    data_requirements: list[str]
    components_used: list[str]
    gaps: list[str]
    timeframes: list[str]
    asset_classes: list[str]
    holding_period: str
    confidence: str
    best_conditions: list[str] = field(default_factory=list)
    stock_types: list[str] = field(default_factory=list)
    tuning: dict = field(default_factory=lambda: {"sl_mult": 3.0, "tp_mult": 4.0, "atr_period": 14})

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "creator": self.creator,
            "category": self.category,
            "description": self.description,
            "core_concepts": self.core_concepts,
            "data_requirements": self.data_requirements,
            "components_used": self.components_used,
            "gaps": self.gaps,
            "timeframes": self.timeframes,
            "asset_classes": self.asset_classes,
            "holding_period": self.holding_period,
            "confidence": self.confidence,
            "best_conditions": self.best_conditions,
            "stock_types": self.stock_types,
            "tuning": self.tuning,
        }


STRATEGIES: dict[str, Strategy] = {}


def register(s: Strategy):
    STRATEGIES[s.name] = s


def get(name: str) -> Strategy | None:
    return STRATEGIES.get(name)


def find_by_condition(day_type: str) -> list[Strategy]:
    return [s for s in STRATEGIES.values() if day_type in s.best_conditions]


def find_by_stock_type(stock_type: str) -> list[Strategy]:
    return [s for s in STRATEGIES.values() if stock_type in s.stock_types]


def list_by_category(category: str) -> list[Strategy]:
    return [s for s in STRATEGIES.values() if s.category == category]


# ═══════════════════════════════════════════════════════════════
# 1. Smart Money / Institutional Concepts
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="ICT — Inner Circle Trader",
    creator="Michael J. Huddleston",
    category="Smart Money / Institutional",
    description="ICT concepts for market structure, liquidity, and entry timing. Used mainly for forex, indices, and futures intraday trading.",
    core_concepts=["MSS", "BOS", "CHOCH", "FVG", "Order Blocks", "Liquidity Sweeps",
                   "Buy-side/Sell-side Liquidity", "Premium & Discount Zones", "OTE",
                   "Kill Zones", "Power of Three", "Accumulation → Manipulation → Distribution"],
    data_requirements=["OHLCV", "Swing highs/lows", "ATR", "Structure events (BOS/CHOCH)"],
    components_used=["engines/market_structure.py", "engines/fvg_engine.py",
                     "engines/liquidity_engine.py", "engines/premium_discount_engine.py",
                     "engines/smc_engine.py", "policies/origin_region/ict/*.py",
                     "policies/fair_value_gap/ict/*.py",
                     "policies/order_block/ict/*.py",
                     "domain/reasoning/ict/*.py",
                     "domain/execution/ict_execution_planner.py",
                     "engines/market_state_engine.py"],
    gaps=["Kill Zones detection (London/NY open)", "OTE Fibonacci zones",
          "Power of Three pattern recognition", "Order flow tape reading"],
    timeframes=["1m", "5m", "15m", "1h"],
    asset_classes=["forex", "indices", "futures", "options"],
    holding_period="Intraday to Swing",
    confidence="PARTIAL",
    best_conditions=["TREND_UP", "TREND_DOWN", "RANGE", "GAP_UP", "GAP_DOWN"],
    stock_types=["RS_LEADER", "FOLLOWER", "IN_LINE"],
    tuning={"sl_mult": 3.0, "tp_mult": 4.0, "atr_period": 14},
))

register(Strategy(
    name="Smart Money Concepts (SMC)",
    creator="Various (evolved from ICT)",
    category="Smart Money / Institutional",
    description="Broader than ICT. Focuses on institutional order flow, liquidity grabs, mitigation blocks, breaker blocks, and supply/demand zones.",
    core_concepts=["Institutional Order Flow", "Liquidity Grabs", "Mitigation Blocks",
                   "Breaker Blocks", "Imbalance", "Supply/Demand Zones",
                   "Inducement", "Market Structure Mapping"],
    data_requirements=["OHLCV", "Swing highs/lows", "Liquidity sweeps", "Order blocks"],
    components_used=["engines/liquidity_engine.py", "engines/smc_engine.py",
                     "engines/order_block_engine.py", "engines/market_structure.py",
                     "engines/premium_discount_engine.py"],
    gaps=["Breaker block detection", "Mitigation block detection",
          "Supply/demand zone mapping", "Composite operator analysis"],
    timeframes=["15m", "1h", "4h", "1d"],
    asset_classes=["forex", "indices", "futures", "equity"],
    holding_period="Swing to Position",
    confidence="PARTIAL",
    best_conditions=["TREND_UP", "TREND_DOWN", "REVERSAL"],
    stock_types=["RS_LEADER", "FOLLOWER", "IN_LINE"],
))

register(Strategy(
    name="Wyckoff Method",
    creator="Richard Wyckoff",
    category="Smart Money / Institutional",
    description="Institutional-style accumulation/distribution analysis. Identifies composite operator activity through price and volume.",
    core_concepts=["Accumulation", "Distribution", "Markup", "Markdown",
                   "Composite Operator", "Spring", "Upthrust",
                   "Sign of Strength (SOS)", "Last Point of Support (LPS)"],
    data_requirements=["OHLCV", "Volume", "Swing structure"],
    components_used=[],
    gaps=["Complete — Spring/Upthrust detection", "Accumulation/distribution pattern recognition",
          "Composite Operator simulation", "LPS/LPSY identification",
          "SOS/SOW confirmation", "Wyckoff phase progression"],
    timeframes=["1h", "4h", "1d", "1w"],
    asset_classes=["equity", "indices", "futures"],
    holding_period="Swing to Position",
    confidence="NOT_STARTED",
    best_conditions=["REVERSAL", "RANGE"],
    stock_types=["IN_LINE", "WEAKNESS", "DEFENSIVE"],
))

# ═══════════════════════════════════════════════════════════════
# 2. Momentum / Growth Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="CAN SLIM",
    creator="William J. O'Neil",
    category="Momentum / Growth",
    description="Seven-factor growth stock selection framework: Current earnings, Annual earnings, New products, Supply & demand, Leader stocks, Institutional sponsorship, Market direction.",
    core_concepts=["C-Current Earnings", "A-Annual Earnings", "N-New Products/Highs",
                   "S-Supply & Demand", "L-Leader Stocks", "I-Institutional Sponsorship",
                   "M-Market Direction"],
    data_requirements=["Quarterly earnings", "Annual earnings", "EPS growth",
                       "RS rating", "Volume", "Institutional ownership", "Industry group rank"],
    components_used=[],
    gaps=["Complete — Earnings data integration (screener.in/finviz)",
          "EPS rating calculation", "RS rating calculation",
          "Industry group ranking", "Institutional sponsorship tracker",
          "Market direction confirmation"],
    timeframes=["1d", "1w"],
    asset_classes=["equity"],
    holding_period="Swing to Long-Term",
    confidence="NOT_STARTED",
    best_conditions=["TREND_UP", "GAP_UP"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
))

register(Strategy(
    name="Mark Minervini SEPA Strategy",
    creator="Mark Minervini",
    category="Momentum / Growth",
    description="Specific Entry Point Analysis — Volatility Contraction Patterns (VCP) with Stage 2 uptrend, high relative strength, and institutional accumulation.",
    core_concepts=["VCP (Volatility Contraction Pattern)", "Stage 2 Uptrend",
                   "Relative Strength", "Institutional Accumulation",
                   "Tight Bases", "Breakout Entries"],
    data_requirements=["OHLCV", "RS rating", "Volume analysis",
                       "ATR contraction", "EMA structure"],
    components_used=["feature_engine/features/volatility.py",
                     "feature_engine/features/trend.py",
                     "feature_engine/features/momentum.py"],
    gaps=["VCP pattern detection (contracting range + volume)", "Stage analysis (1-4)",
          "RS ranking vs all stocks", "Base count and depth measurement",
          "Tightness scoring algorithm"],
    timeframes=["1d", "1w"],
    asset_classes=["equity"],
    holding_period="Swing to 3-6 months",
    confidence="PLANNED",
    best_conditions=["TREND_UP", "GAP_UP"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
    tuning={"sl_mult": 2.0, "tp_mult": 3.0, "min_vcp_contraction": 0.3},
))

register(Strategy(
    name="Momentum Trading",
    creator="Various",
    category="Momentum / Growth",
    description="Strong stocks continue moving strongly. Uses relative strength, breakouts, volume expansion, 52-week highs, and sector leadership.",
    core_concepts=["Relative Strength", "Breakouts", "Volume Expansion",
                   "52-week highs", "Sector Leadership", "Moving Averages"],
    data_requirements=["OHLCV", "RSI", "Volume", "Moving averages",
                       "52-week high/low", "Sector data"],
    components_used=["engines/indicator_engine.py",
                     "feature_engine/features/momentum.py",
                     "feature_engine/features/trend.py",
                     "feature_engine/features/volume.py",
                     "feature_engine/features/volatility.py"],
    gaps=["52-week high breakout detection", "Sector leadership ranking",
          "Relative strength ranking vs all stocks",
          "Momentum score calculation", "Pullback vs breakdown filter"],
    timeframes=["15m", "1h", "1d"],
    asset_classes=["equity", "indices", "futures", "crypto"],
    holding_period="Intraday to Swing",
    confidence="PARTIAL",
    best_conditions=["TREND_UP", "GAP_UP"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
    tuning={"sl_mult": 3.0, "tp_mult": 3.5, "min_volume_ratio": 1.5},
))

register(Strategy(
    name="Darvas Box Theory",
    creator="Nicolas Darvas",
    category="Momentum / Growth",
    description="Box consolidation pattern breakout strategy. Focuses on new highs with volume confirmation in trending stocks.",
    core_concepts=["Box Consolidation", "New Highs", "Breakout Confirmation",
                   "Volume Expansion", "Trailing Stops"],
    data_requirements=["OHLCV", "Volume", "Swing highs/lows"],
    components_used=[],
    gaps=["Complete — Box pattern detection", "Box depth measurement",
          "Breakout from box confirmation", "Trailing stop implementation"],
    timeframes=["1d"],
    asset_classes=["equity"],
    holding_period="Swing",
    confidence="NOT_STARTED",
    best_conditions=["TREND_UP", "GAP_UP"],
    stock_types=["BREAKOUT", "RS_LEADER"],
))

# ═══════════════════════════════════════════════════════════════
# 3. Trend Following
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Trend Following",
    creator="Various (Ed Seykota, Richard Dennis, etc.)",
    category="Trend Following",
    description="Ride big trends, cut losses quickly. Uses moving averages, breakouts, Donchian Channels, and ATR trailing stops. Example: Turtle Trading.",
    core_concepts=["Ride Big Trends", "Cut Losses", "Moving Averages",
                   "Breakouts from Donchian Channels", "ATR Trailing Stops",
                   "Pyramiding"],
    data_requirements=["OHLCV", "Moving averages", "Donchian Channels", "ATR"],
    components_used=["engines/indicator_engine.py",
                     "feature_engine/features/trend.py",
                     "feature_engine/features/momentum.py"],
    gaps=["Donchian Channel implementation", "ATR trailing stop logic",
          "Pyramiding rules", "Trend filter (ADX or similar)",
          "Entry/exit systematic rules"],
    timeframes=["1d", "1w", "1mo"],
    asset_classes=["equity", "indices", "futures", "commodities"],
    holding_period="Swing to Long-Term",
    confidence="PLANNED",
    best_conditions=["TREND_UP", "TREND_DOWN"],
    stock_types=["RS_LEADER", "FOLLOWER"],
    tuning={"entry_channel": 20, "exit_channel": 10, "atr_mult": 3.0},
))

# ═══════════════════════════════════════════════════════════════
# 4. Mean Reversion
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Mean Reversion Trading",
    creator="Various",
    category="Mean Reversion",
    description="Extreme moves return toward average. Uses RSI extremes, Bollinger Bands, VWAP deviation, and statistical z-scores.",
    core_concepts=["RSI Extremes", "Bollinger Bands", "VWAP Deviation",
                   "Statistical Z-Score", "Pullback to EMAs"],
    data_requirements=["OHLCV", "RSI", "Bollinger Bands", "VWAP", "Standard deviation"],
    components_used=["feature_engine/features/momentum.py",
                     "engines/indicator_engine.py"],
    gaps=["Bollinger Band implementation", "Z-score calculation",
          "VWAP deviation entry rules",
          "Mean reversion confirmation filter",
          "Stop placement for reversion trades"],
    timeframes=["15m", "1h", "1d"],
    asset_classes=["equity", "indices", "futures"],
    holding_period="Intraday to Swing",
    confidence="PLANNED",
    best_conditions=["RANGE", "CHOPPY"],
    stock_types=["IN_LINE", "WEAKNESS"],
    tuning={"rsi_oversold": 30, "rsi_overbought": 70, "bb_mult": 2.0},
))

# ═══════════════════════════════════════════════════════════════
# 5. Price Action / Technical Analysis
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Price Action Trading",
    creator="Various (Al Brooks, Naked Trading)",
    category="Price Action / Technical Analysis",
    description="Pure chart reading using support/resistance, candlestick patterns, trendlines, channels, breakouts, and retests.",
    core_concepts=["Support/Resistance", "Candlestick Patterns", "Trendlines",
                   "Channels", "Breakouts", "Retests",
                   "Pin Bars", "Inside Bars", "Engulfing Patterns"],
    data_requirements=["OHLCV", "Swing points"],
    components_used=["engines/market_structure.py",
                     "engines/swing_engine.py",
                     "feature_engine/features/price.py",
                     "engines/liquidity_engine.py"],
    gaps=["Candlestick pattern recognition (pin bar, engulfing, inside bar)",
          "Trendline drawing/break detection", "Channel detection",
          "Retest confirmation logic", "Multiple timeframe confluence"],
    timeframes=["5m", "15m", "1h", "1d"],
    asset_classes=["equity", "forex", "indices", "futures"],
    holding_period="Intraday to Swing",
    confidence="PARTIAL",
    best_conditions=["RANGE", "TREND_UP", "TREND_DOWN"],
    stock_types=["IN_LINE", "RS_LEADER"],
))

# ═══════════════════════════════════════════════════════════════
# 6. Volume-Based Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Volume Price Analysis (VPA)",
    creator="Richard Ney, Tom Williams, Anna Coulling",
    category="Volume-Based",
    description="Price + volume relationship analysis. Identifies effort vs result, climactic volume, absorption, and no-demand candles.",
    core_concepts=["Effort vs Result", "Climactic Volume", "Absorption",
                   "No Demand Candles", "No Supply Candles",
                   "Volume Confirmation", "Volume Divergence"],
    data_requirements=["OHLCV", "Volume"],
    components_used=["feature_engine/features/volume.py"],
    gaps=["Complete — Effort vs result calculation", "Climactic volume detection",
          "Absorption pattern recognition",
          "Volume divergence with price",
          "VPA bar-by-bar classification"],
    timeframes=["15m", "1h", "1d"],
    asset_classes=["equity", "indices", "futures"],
    holding_period="Intraday to Swing",
    confidence="PLANNED",
    best_conditions=["ALL"],
    stock_types=["ALL"],
))

register(Strategy(
    name="Volume Profile Trading",
    creator="Peter Steidlmayer, Jim Dalton",
    category="Volume-Based",
    description="Market profile analysis using Point of Control (POC), Value Area High/Low (VAH/VAL), high/low volume nodes for futures trading.",
    core_concepts=["Point of Control (POC)", "Value Area High (VAH)",
                   "Value Area Low (VAL)", "High Volume Nodes",
                   "Low Volume Nodes", "Volume Profile Shapes"],
    data_requirements=["OHLCV", "Volume profile data (tick/volume per price)"],
    components_used=[],
    gaps=["Complete — Volume profile construction", "POC detection",
          "Value Area calculation (70% of volume)",
          "High/Low volume node identification",
          "Profile shape classification (D, P, b, B shapes)"],
    timeframes=["Intraday"],
    asset_classes=["futures", "equity"],
    holding_period="Intraday",
    confidence="NOT_STARTED",
    best_conditions=["RANGE", "TREND_UP", "TREND_DOWN"],
    stock_types=["ALL"],
))

register(Strategy(
    name="Market Profile",
    creator="J. Peter Steidlmayer",
    category="Volume-Based",
    description="Auction Market Theory: balance vs imbalance, Initial Balance, TPO profiles. Used by professional futures traders.",
    core_concepts=["Auction Market Theory", "Balance vs Imbalance",
                   "Initial Balance", "TPO Profiles", "Value Area",
                   "Single Prints", "Excess"],
    data_requirements=["OHLCV", "Time-price-opportunity data", "Volume"],
    components_used=[],
    gaps=["Complete — TPO profile construction",
          "Initial Balance detection", "Value Area from TPO",
          "Single print/excess detection",
          "Balance vs imbalance classification"],
    timeframes=["Intraday"],
    asset_classes=["futures", "equity"],
    holding_period="Intraday",
    confidence="NOT_STARTED",
    best_conditions=["ALL"],
    stock_types=["ALL"],
))

# ═══════════════════════════════════════════════════════════════
# 7. Execution / Intraday Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Opening Range Breakout (ORB)",
    creator="Toby Crabel",
    category="Execution / Intraday",
    description="Define first 5/15/30 minute range, trade breakout with volume confirmation and trend continuation.",
    core_concepts=["First 30-min Range", "Breakout", "Volume Confirmation",
                   "VWAP Filter", "Sector Confirmation",
                   "Trend Continuation"],
    data_requirements=["OHLCV", "First 30m range", "VWAP", "Volume", "Sector data"],
    components_used=[],
    gaps=["Complete — First N-minute range calculation",
          "ORB breakout detection with volume filter",
          "VWAP + sector confirmation",
          "Trailing stop for ORB trades",
          "Opening range type classification (wide/narrow)"],
    timeframes=["1m", "5m", "15m"],
    asset_classes=["equity", "futures"],
    holding_period="Intraday",
    confidence="NOT_STARTED",
    best_conditions=["TREND_UP", "TREND_DOWN", "GAP_UP", "GAP_DOWN"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
    tuning={"sl_mult": 1.5, "tp_mult": 2.0, "min_vol_ratio": 2.0},
))

register(Strategy(
    name="VWAP Pullback Strategy",
    creator="Various",
    category="Execution / Intraday",
    description="Higher accuracy entry by waiting for pullback to VWAP after breakout. Requires rising VWAP and 20 EMA support.",
    core_concepts=["VWAP Retest", "Rising VWAP", "20 EMA Support",
                   "Low Volume Pullback", "Trend Continuation"],
    data_requirements=["OHLCV", "VWAP", "EMA 20", "Volume"],
    components_used=["engines/indicator_engine.py",
                     "engines/risk_engine.py"],
    gaps=["Complete — VWAP retest detection",
          "Low volume pullback filter",
          "EMA support confirmation",
          "VWAP slope direction tracking",
          "Entry trigger after pullback"],
    timeframes=["5m", "15m", "1h"],
    asset_classes=["equity", "futures"],
    holding_period="Intraday",
    confidence="PLANNED",
    best_conditions=["TREND_UP", "TREND_DOWN"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
    tuning={"sl_mult": 2.0, "tp_mult": 3.0, "vwap_bounce_min": 0.1},
))

register(Strategy(
    name="Scalping",
    creator="Various",
    category="Execution / Intraday",
    description="Very short-term trading using order flow, tape reading, Level 2 data, VWAP, and liquidity.",
    core_concepts=["Order Flow", "Tape Reading", "Level 2 Data",
                   "VWAP", "Liquidity", "Bid/Ask Imbalance",
                   "Market Microstructure"],
    data_requirements=["Tick data", "Level 2 order book", "VWAP", "Bid/ask spread"],
    components_used=[],
    gaps=["Complete — Requires order book / tick data feed",
          "Not suitable for current yfinance/Upstox REST setup"],
    timeframes=["1m", "Tick"],
    asset_classes=["equity", "futures", "forex"],
    holding_period="Seconds to Minutes",
    confidence="NOT_STARTED",
    best_conditions=["RANGE", "CHOPPY"],
    stock_types=["ALL"],
))

# ═══════════════════════════════════════════════════════════════
# 8. Quantitative / Statistical Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Quantitative Trading",
    creator="Various",
    category="Quantitative / Statistical",
    description="Math/statistics-based trading including factor investing, statistical arbitrage, momentum factors, mean reversion models, and ML models.",
    core_concepts=["Factor Investing", "Statistical Arbitrage",
                   "Momentum Factors", "Mean Reversion Models",
                   "Machine Learning", "Backtesting",
                   "Risk Factor Models"],
    data_requirements=["OHLCV", "Fundamental data", "Alternative data",
                       "Multiple securities history", "Python/statistical libraries"],
    components_used=["backtesting/engine.py", "backtesting/metrics.py",
                     "backtesting/report.py", "experiments/*.py",
                     "feature_engine/feature_registry.py"],
    gaps=["Factor construction and testing", "Statistical arbitrage pair selection",
          "Risk model implementation", "ML model pipeline",
          "Walk-forward optimization framework"],
    timeframes=["All"],
    asset_classes=["All"],
    holding_period="All",
    confidence="PARTIAL",
    best_conditions=["ALL"],
    stock_types=["ALL"],
))

register(Strategy(
    name="Pairs Trading",
    creator="Various (Morgan Stanley quant desk origin)",
    category="Quantitative / Statistical",
    description="Market-neutral strategy trading two historically correlated securities when they diverge. Long the laggard, short the leader.",
    core_concepts=["Cointegration", "Correlation", "Spread Mean Reversion",
                   "Z-Score Entry", "Market Neutral",
                   "Beta Adjustment"],
    data_requirements=["OHLCV for 2+ correlated securities", "Cointegration testing",
                       "Z-score calculation"],
    components_used=[],
    gaps=["Complete — Pair selection algorithm", "Cointegration testing",
          "Spread calculation and normalization",
          "Entry/exit threshold rules",
          "Portfolio of pairs management"],
    timeframes=["1h", "1d"],
    asset_classes=["equity", "futures"],
    holding_period="Days to Weeks",
    confidence="NOT_STARTED",
    best_conditions=["RANGE", "CHOPPY"],
    stock_types=["IN_LINE"],
))

register(Strategy(
    name="Arbitrage Strategies",
    creator="Various",
    category="Quantitative / Statistical",
    description="Risk-free or near-risk-free profit from price discrepancies: cash-futures, index, merger, statistical arbitrage. Mostly institutional.",
    core_concepts=["Cash-Futures Arbitrage", "Index Arbitrage",
                   "Merger Arbitrage", "Statistical Arbitrage",
                   "Risk-Free Profit", "Price Discrepancy"],
    data_requirements=["Futures and spot prices", "Multiple exchange data",
                       "Corporate action data", "Low-latency feeds"],
    components_used=[],
    gaps=["Complete — Requires multi-asset data feeds",
          "Not suitable for current retail setup"],
    timeframes="Intraday to Days",
    asset_classes=["equity", "futures", "options"],
    holding_period="Seconds to Days",
    confidence="NOT_STARTED",
    best_conditions=["ALL"],
    stock_types=["ALL"],
))

# ═══════════════════════════════════════════════════════════════
# 9. Options Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Options Strategies",
    creator="Various",
    category="Options",
    description="Multi-leg options strategies for various market conditions: Covered Call, Protective Put, Iron Condor, Butterfly, Straddle, Strangle, Calendar Spread.",
    core_concepts=["Covered Call", "Protective Put", "Iron Condor",
                   "Butterfly", "Straddle", "Strangle",
                   "Calendar Spread", "Implied Volatility",
                   "Greeks (Delta, Gamma, Theta, Vega)"],
    data_requirements=["Options chain data", "Underlying price", "IV data",
                       "Greeks", "Expiry calendar"],
    components_used=[],
    gaps=["Complete — Requires options data feed",
          "Not suitable for current equity focus"],
    timeframes=["All"],
    asset_classes=["options", "equity"],
    holding_period="Days to Weeks",
    confidence="NOT_STARTED",
    best_conditions=["ALL"],
    stock_types=["ALL"],
))

# ═══════════════════════════════════════════════════════════════
# 10. Event-Driven Strategies
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Event Driven Trading",
    creator="Various",
    category="Event-Driven",
    description="Trades based on earnings, news, M&A, policy changes, results, and guidance changes. Momentum continuation or reaction trading.",
    core_concepts=["Earnings Trades", "News Trading", "M&A Arbitrage",
                   "Policy/Macro Trades", "Result Reactions",
                   "Guidance Changes"],
    data_requirements=["Earnings calendar", "News feed", "Economic calendar",
                       "Corporate action data", "Real-time news"],
    components_used=[],
    gaps=["Complete — Requires event data integration",
          "Not suitable for current technical-only setup"],
    timeframes=["1m to 1d"],
    asset_classes=["equity", "indices", "forex"],
    holding_period="Minutes to Weeks",
    confidence="NOT_STARTED",
    best_conditions=["GAP_UP", "GAP_DOWN", "REVERSAL"],
    stock_types=["BREAKOUT", "BREAKDOWN"],
))

# ═══════════════════════════════════════════════════════════════
# 11. Professional Equity Momentum (Combined)
# ═══════════════════════════════════════════════════════════════

register(Strategy(
    name="Professional Equity Momentum",
    creator="Institutional Best Practices",
    category="Momentum / Growth",
    description="Closest to what institutional equity traders do. Combines market direction, sector strength, relative strength, volume expansion, and VWAP execution. Core of the top-gainer prediction system.",
    core_concepts=["Market Direction", "Sector Leadership", "Relative Strength",
                   "Volume Expansion", "Breakout/Continuation", "VWAP Execution",
                   "Institutional Flow Capture"],
    data_requirements=["OHLCV", "Sector data", "VWAP", "Volume ratio",
                       "RS ranking", "Market context (NIFTY)"],
    components_used=["engines/day_type_engine.py", "engines/stock_type_engine.py",
                     "services/ict_analysis_service.py",
                     "engines/market_structure.py",
                     "engines/signal_engine.py",
                     "engines/risk_engine.py",
                     "engines/confluence_engine.py",
                     "engines/probability_engine.py",
                     "feature_engine/features/*.py"],
    gaps=["Sector scoring algorithm", "RS ranking vs all NSE stocks",
          "Systematic watchlist filtering",
          "False breakout rate tracking",
          "Morning gap-up vs gap-down classification"],
    timeframes=["15m", "1h", "1d"],
    asset_classes=["equity"],
    holding_period="Intraday to Swing",
    confidence="IMPLEMENTED",
    best_conditions=["TREND_UP", "GAP_UP", "REVERSAL"],
    stock_types=["RS_LEADER", "BREAKOUT", "FOLLOWER"],
    tuning={"sl_mult": 3.0, "tp_mult": 4.0, "atr_period": 14, "min_vol_ratio": 1.5},
))

register(Strategy(
    name="Institutional Probability",
    creator="Institutional Best Practices",
    category="Momentum / Growth",
    description="Timeframe-agnostic 8-factor institutional scoring engine. Scores setups 0-100 across Market Regime, Sector Strength, Price Action, Volume, Breakout Quality, Risk/Reward, Indicators, and Catalyst. Trades only when score >= 80.",
    core_concepts=["8-Factor Scoring", "Market Regime", "Sector Strength",
                   "Price Action", "Volume Analysis", "Breakout Quality",
                   "Risk/Reward", "Indicator Confluence", "Smart Money"],
    data_requirements=["OHLCV", "NIFTY data", "Volume", "ATR",
                       "Sector mapping", "Day/Stock type"],
    components_used=["engines/institutional_probability_engine.py",
                     "engines/market_regime_engine.py",
                     "engines/sector_rotation_engine.py",
                     "engines/market_structure.py",
                     "engines/risk_engine.py"],
    gaps=["Sector ETF live data feed", "Real-time FII/DII integration",
          "News catalyst scoring"],
    timeframes=["1m", "15m", "1h", "1d"],
    asset_classes=["equity"],
    holding_period="Intraday to Swing",
    confidence="IMPLEMENTED",
    best_conditions=["ALL"],
    stock_types=["ALL"],
    tuning={"sl_mult": 0.5, "tp_mult": 5.0, "atr_period": 14,
            "short_sl_mult": 3.0, "short_tp_mult": 1.5},
))
