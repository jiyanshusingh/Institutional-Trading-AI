from engines.position_engine import PositionEngine

engine = PositionEngine()

result = engine.calculate(
    entry=800,
    stoploss=780,
    capital=200000,
    risk_percent=1
)

print(result)