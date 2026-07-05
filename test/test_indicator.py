from engines.data_engine import DataEngine
from engines.indicator_engine import IndicatorEngine

engine = DataEngine()
indicator = IndicatorEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

df = indicator.calculate(df)

print(df.tail())