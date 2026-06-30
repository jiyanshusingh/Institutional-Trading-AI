from services.analysis_service import analyze_stock
from engines.rating_engine import RatingEngine

result = analyze_stock("MARICO.NS")

engine = RatingEngine(
    result["signal"],
    result["probability"],
    result["confluence"]
)

print(engine.calculate())