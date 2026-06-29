from engines.data_engine import DataEngine

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:", df.shape)