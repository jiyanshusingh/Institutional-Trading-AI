from services.analysis_service import analyze_stock
from engines.probability_engine import ProbabilityEngine

result = analyze_stock("MARICO.NS")

engine = ProbabilityEngine(
    result["df"],
    result["signal"]
)

prob = engine.calculate()

print(prob)