from services.analysis_service import analyze_stock


class ScannerEngine:

    def scan(self, symbols):

        results = []

        for symbol in symbols:

            try:
                result = analyze_stock(symbol)

                signal = result["signal"]
                trade = result["risk"]

                results.append({
                    "Stock": symbol,
                    "Signal": signal["Signal"],
                    "Score": signal["Score"],
                    "Entry": trade["Entry"],
                    "Target": trade["Target1"],
                    "RR": trade["RR"]
                })

            except Exception as e:
                print(f"{symbol} -> {e}")

        results.sort(
            key=lambda x: x["Score"],
            reverse=True
        )

        return results