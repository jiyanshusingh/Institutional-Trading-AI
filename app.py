from services.analysis_service import analyze_stock

symbol = "MARICO.NS"

result = analyze_stock(symbol)

print("=" * 60)
print("Institutional Trading AI")
print("=" * 60)

print(f"\nStock : {result['symbol']}")
print(f"Signal : {result['signal']['Signal']}")
print(f"Score : {result['signal']['Score']}")

print("\nReasons:")

for reason in result["signal"]["Reasons"]:
    print(f"✓ {reason}")

print("\nTrade Setup")
print("-" * 30)

print(f"Entry      : {result['risk']['Entry']}")
print(f"Stop Loss  : {result['risk']['StopLoss']}")
print(f"Target 1   : {result['risk']['Target1']}")
print(f"Target 2   : {result['risk']['Target2']}")
print(f"Risk/Reward: {result['risk']['RR']}:1")
