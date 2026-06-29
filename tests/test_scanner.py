from engines.scanner_engine import ScannerEngine
from data.stocks import NSE_STOCKS

scanner = ScannerEngine()

results = scanner.scan(NSE_STOCKS)

for stock in results:

    print(stock)
from pprint import pprint

for stock in results:
    pprint(stock)