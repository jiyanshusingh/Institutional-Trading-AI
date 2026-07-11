import pandas as pd
import requests
import gzip
import shutil


url = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv.gz"


response = requests.get(url)

with open("NSE.csv.gz","wb") as f:
    f.write(response.content)


with gzip.open("NSE.csv.gz","rb") as f_in:
    with open("NSE.csv","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)


df = pd.read_csv("NSE.csv")


print(df.head())

print(df.columns)