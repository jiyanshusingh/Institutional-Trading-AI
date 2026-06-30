from services.analysis_service import analyze_stock


class MultiTimeframeEngine:

    def analyze(self, symbol):

        timeframes = {

            "15m": ("30d", "15m"),

            "1h": ("730d", "60m"),

            "1d": ("1y", "1d")

        }

        results = {}

        for tf, (period, interval) in timeframes.items():

            try:
                result = analyze_stock(
                    symbol,
                    period=period,
                    interval=interval
                )

                results[tf] = result["signal"]["Signal"]

            except Exception as e:
                print(f"{tf} failed: {e}")
                results[tf] = "Unavailable"
        return results