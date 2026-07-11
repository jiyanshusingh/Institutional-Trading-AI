"""
Strategy Selector

Maps (day_type, stock_type) → recommended strategy + tuning params.

The selector matrix encodes domain expertise about which strategies
perform best in which market conditions for which stock types.
"""

from __future__ import annotations

from strategies.registry import STRATEGIES, Strategy, get


# ═══════════════════════════════════════════════════════════════
# Selection Matrix
#
# Maps: (day_type, stock_type) → (strategy_name, rationale)
# ═══════════════════════════════════════════════════════════════

SELECTION_MATRIX: dict[tuple[str, str], tuple[str, str]] = {
    # ── Trend Up Days ──────────────────────────────────────
    ("TREND_UP", "RS_LEADER"): (
        "Momentum Trading",
        "Strong trend with leading stock — capture institutional flow with momentum breakout.",
    ),
    ("TREND_UP", "BREAKOUT"): (
        "Professional Equity Momentum",
        "Breakout structure in trending market — highest probability continuation setup.",
    ),
    ("TREND_UP", "FOLLOWER"): (
        "VWAP Pullback Strategy",
        "Trend up but stock is following — wait for VWAP pullback for lower-risk entry.",
    ),
    ("TREND_UP", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Trend up with defensive stock — VWAP pullback offers safe entry in strong market.",
    ),
    ("TREND_UP", "IN_LINE"): (
        "ICT — Inner Circle Trader",
        "Stock tracking market, use ICT structure for precision entry on pullbacks.",
    ),
    ("TREND_UP", "WEAKNESS"): (
        "Mean Reversion Trading",
        "Stock weak while market strong — potential reversal or avoid.",
    ),
    ("TREND_UP", "BREAKDOWN"): (
        "Mean Reversion Trading",
        "Stock breaking down in strong market — divergence, expect reversion to trend.",
    ),

    # ── Trend Down Days ────────────────────────────────────
    ("TREND_DOWN", "WEAKNESS"): (
        "Trend Following",
        "Market trending down with weak stock — short-side momentum.",
    ),
    ("TREND_DOWN", "IN_LINE"): (
        "ICT — Inner Circle Trader",
        "Bearish structure — wait for FVG/liquidity grab before short entry.",
    ),
    ("TREND_DOWN", "RS_LEADER"): (
        "Mean Reversion Trading",
        "Stock strong while market weak — potential relative strength reversal.",
    ),
    ("TREND_DOWN", "FOLLOWER"): (
        "ICT — Inner Circle Trader",
        "Market down, stock following — ICT structure for precision short entries.",
    ),
    ("TREND_DOWN", "BREAKOUT"): (
        "Mean Reversion Trading",
        "Stock breaking out while market trends down — divergence, expect mean reversion.",
    ),
    ("TREND_DOWN", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Defensive stock holds better in downtrend — wait for controlled VWAP entries.",
    ),
    ("TREND_DOWN", "BREAKDOWN"): (
        "Trend Following",
        "Market down + stock breaking down — momentum short with trend confirmation.",
    ),

    # ── Range Days ─────────────────────────────────────────
    ("RANGE", "IN_LINE"): (
        "Price Action Trading",
        "Range day + in-line stock — use swing breaks for entries in direction of range.",
    ),
    ("RANGE", "RS_LEADER"): (
        "Price Action Trading",
        "Stock showing relative strength in range — wait for compression breakout.",
    ),
    ("RANGE", "BREAKOUT"): (
        "Price Action Trading",
        "Stock breaking out while market ranges — use price action for confirmation.",
    ),
    ("RANGE", "WEAKNESS"): (
        "Price Action Trading",
        "Weak in range — use price action swings for entries in direction of range.",
    ),
    ("RANGE", "FOLLOWER"): (
        "Price Action Trading",
        "Range day, stock following — trade range swings with price action signals.",
    ),
    ("RANGE", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Defensive stock in range — use VWAP pullbacks for safer entries.",
    ),
    ("RANGE", "BREAKDOWN"): (
        "Trend Following",
        "Stock breaking down in range — short-side momentum in direction of breakdown.",
    ),

    # ── Gap-Up Days ────────────────────────────────────────
    ("GAP_UP", "RS_LEADER"): (
        "Opening Range Breakout (ORB)",
        "Gap-up with leader stock — use ORB for continuation entry.",
    ),
    ("GAP_UP", "BREAKOUT"): (
        "Professional Equity Momentum",
        "Gap-up breakout — momentum continuation with volume confirmation.",
    ),
    ("GAP_UP", "FOLLOWER"): (
        "VWAP Pullback Strategy",
        "Gap-up but following — wait for VWAP retest, don't chase.",
    ),
    ("GAP_UP", "WEAKNESS"): (
        "ICT — Inner Circle Trader",
        "Gap-up but stock weak — watch for liquidity grab and reversal.",
    ),
    ("GAP_UP", "DEFENSIVE"): (
        "Professional Equity Momentum",
        "Gap-up with defensive stock — momentum entry with volume confirmation.",
    ),
    ("GAP_UP", "IN_LINE"): (
        "Professional Equity Momentum",
        "Gap-up, stock in line — momentum continuation on strong open.",
    ),
    ("GAP_UP", "BREAKDOWN"): (
        "Mean Reversion Trading",
        "Gap-up but stock breaking down — expect reversion from extreme.",
    ),

    # ── Gap-Down Days ──────────────────────────────────────
    ("GAP_DOWN", "WEAKNESS"): (
        "Trend Following",
        "Gap-down with weak stock — short-side momentum.",
    ),
    ("GAP_DOWN", "BREAKDOWN"): (
        "Opening Range Breakout (ORB)",
        "Gap-down breakdown — short ORB continuation.",
    ),
    ("GAP_DOWN", "RS_LEADER"): (
        "Mean Reversion Trading",
        "Gap-down but stock normally strong — potential reversal play.",
    ),
    ("GAP_DOWN", "BREAKOUT"): (
        "Mean Reversion Trading",
        "Gap-down but stock breaking out — divergence, expect reversion.",
    ),
    ("GAP_DOWN", "FOLLOWER"): (
        "ICT — Inner Circle Trader",
        "Gap-down, stock following — wait for FVG/liquidity sweep for short entry.",
    ),
    ("GAP_DOWN", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Gap-down with defensive stock — wait for VWAP retest on recovery attempt.",
    ),
    ("GAP_DOWN", "IN_LINE"): (
        "ICT — Inner Circle Trader",
        "Gap-down, stock in line — bearish structure entries with ICT precision.",
    ),

    # ── Reversal Days ──────────────────────────────────────
    ("REVERSAL", "RS_LEADER"): (
        "Professional Equity Momentum",
        "Market reversing with leader stock — early momentum capture.",
    ),
    ("REVERSAL", "WEAKNESS"): (
        "Wyckoff Method",
        "Reversal day with weak stock — check for Wyckoff redistribution.",
    ),
    ("REVERSAL", "IN_LINE"): (
        "ICT — Inner Circle Trader",
        "Reversal structure — look for CHOCH + FVG confirmation.",
    ),
    ("REVERSAL", "BREAKOUT"): (
        "Professional Equity Momentum",
        "Market reversing, stock breaking out — momentum in direction of reversal.",
    ),
    ("REVERSAL", "FOLLOWER"): (
        "VWAP Pullback Strategy",
        "Market reversing, stock following — wait for controlled VWAP entry in new direction.",
    ),
    ("REVERSAL", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Reversal with defensive stock — use VWAP pullback for lower-risk entry.",
    ),
    ("REVERSAL", "BREAKDOWN"): (
        "Trend Following",
        "Market reversing but stock breaking down — trend is your friend, follow breakdown.",
    ),

    # ── Choppy Days ────────────────────────────────────────
    ("CHOPPY", "IN_LINE"): (
        "Price Action Trading",
        "Choppy market — avoid directional bias, use tight levels.",
    ),
    ("CHOPPY", "RS_LEADER"): (
        "Mean Reversion Trading",
        "Choppy but stock showing RS — fade intraday extremes.",
    ),
    ("CHOPPY", "WEAKNESS"): (
        "ICT — Inner Circle Trader",
        "Choppy with weak stock — wait for liquidity sweep + FVG.",
    ),
    ("CHOPPY", "BREAKOUT"): (
        "Price Action Trading",
        "Choppy market, stock breakout — confirm with price action before entry.",
    ),
    ("CHOPPY", "FOLLOWER"): (
        "Price Action Trading",
        "Choppy, stock following — tight levels and swing breaks for entries.",
    ),
    ("CHOPPY", "DEFENSIVE"): (
        "VWAP Pullback Strategy",
        "Choppy market, defensive stock — VWAP pullbacks for safe entries.",
    ),
    ("CHOPPY", "BREAKDOWN"): (
        "Price Action Trading",
        "Choppy, stock breaking down — trade breakdown with tight stops.",
    ),
}


def select(
    day_type: str,
    stock_type: str,
) -> tuple[Strategy | None, str]:
    """Select the best strategy for given day+stock type."""
    key = (day_type, stock_type)
    if key in SELECTION_MATRIX:
        strategy_name, rationale = SELECTION_MATRIX[key]
        strategy = get(strategy_name)
        return strategy, rationale

    # Fallback: find any strategy matching day_type
    candidates = [s for s in STRATEGIES.values() if day_type in s.best_conditions]
    if candidates:
        s = candidates[0]
        return s, f"Default strategy for {day_type} conditions."

    # Ultimate fallback
    return get("Professional Equity Momentum"), "Market conditions unclear — using default conservative strategy."


def select_with_alternatives(
    day_type: str,
    stock_type: str,
    top_n: int = 3,
) -> list[tuple[Strategy | None, str]]:
    """Return top N strategy recommendations with rationales."""
    results = [select(day_type, stock_type)]

    key = (day_type, stock_type)
    if key in SELECTION_MATRIX:
        alt_candidates = [
            s for s in STRATEGIES.values()
            if s.name != results[0][0].name
            and day_type in s.best_conditions
            and (stock_type in s.stock_types or "ALL" in s.stock_types)
        ]
        for s in alt_candidates[:top_n - 1]:
            results.append((s, f"Alternative: {s.name} for {day_type} + {stock_type}."))

    return results


def get_recommended_tuning(day_type: str, stock_type: str) -> dict:
    """Get tuning parameters from recommended strategy.

    Overlays any optimized SL/TP from ``data/optimized_params.json``
    on top of the strategy's default tuning.
    """
    strategy, _ = select(day_type, stock_type)
    tuning = strategy.tuning.copy() if strategy else {"sl_mult": 3.0, "tp_mult": 4.0, "atr_period": 14}

    # Overlay optimized params if available
    try:
        import json as _json
        from pathlib import Path as _Path
        opt_path = _Path("data/optimized_params.json")
        if opt_path.exists():
            opt = _json.loads(opt_path.read_text())
            key = f"{day_type}__{stock_type}"
            if key in opt and "sl_mult" in opt[key] and "tp_mult" in opt[key]:
                tuning["sl_mult"] = opt[key]["sl_mult"]
                tuning["tp_mult"] = opt[key]["tp_mult"]
    except Exception:
        pass

    return tuning


def available_combinations() -> list[tuple[str, str]]:
    """List all (day_type, stock_type) combinations in the matrix."""
    return list(SELECTION_MATRIX.keys())


def suggests_active_trading(day_type: str, stock_type: str) -> bool:
    """Whether the recommended strategy suggests an active trade vs avoidance."""
    strategy, _ = select(day_type, stock_type)
    if strategy is None:
        return False
    avoid_strategies = ["Mean Reversion Trading", "Wyckoff Method"]
    return strategy.confidence != "NOT_STARTED" and strategy.name not in avoid_strategies


# ═══════════════════════════════════════════════════════════════
# Executable Strategy Registry
#
# Maps strategy names → concrete ExecutableStrategy classes that
# can be instantiated and run during backtesting.
# ═══════════════════════════════════════════════════════════════

EXECUTABLE_MAP: dict[str, type] = {}


def register_executable(name: str, strategy_cls: type):
    """Register a strategy name → executable class mapping."""
    EXECUTABLE_MAP[name] = strategy_cls


def get_executable(name: str, **kwargs):
    """Get an instantiated ExecutableStrategy by name."""
    cls = EXECUTABLE_MAP.get(name)
    if cls is None:
        return None
    return cls(**kwargs)


# Register known executable strategies
from strategies.ict_strategy import ICTStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.trend_following_strategy import TrendFollowingStrategy
from strategies.mean_reversion_strategy import MeanReversionStrategy
from strategies.vwap_pullback_strategy import VWAPPullbackStrategy
from strategies.price_action_strategy import PriceActionStrategy
from strategies.orb_strategy import ORBStrategy
from strategies.professional_momentum_strategy import ProfessionalMomentumStrategy

register_executable("ICT — Inner Circle Trader", ICTStrategy)
register_executable("Momentum Trading", MomentumStrategy)
register_executable("Trend Following", TrendFollowingStrategy)
register_executable("Mean Reversion Trading", MeanReversionStrategy)
register_executable("VWAP Pullback Strategy", VWAPPullbackStrategy)
register_executable("Price Action Trading", PriceActionStrategy)
register_executable("Opening Range Breakout (ORB)", ORBStrategy)
register_executable("Professional Equity Momentum", ProfessionalMomentumStrategy)
from strategies.institutional_strategy import InstitutionalStrategy
register_executable("Institutional Probability", InstitutionalStrategy)
