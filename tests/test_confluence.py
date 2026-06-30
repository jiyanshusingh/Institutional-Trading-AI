from services.analysis_service import analyze_stock
from engines.confluence_engine import ConfluenceEngine

result = analyze_stock("MARICO.NS")

engine = ConfluenceEngine(
    result["df"],
    result["signal"]
)

print(engine.calculate())