from services.analysis_service import analyze_stock

result = analyze_stock("MARICO.NS")

print(result["signal"])
print(result["trade"])