import yfinance as yf
import pandas as pd
from pprint import pprint


msft = yf.Ticker("MSFT")
df = pd.DataFrame(msft.history(period="10y"))
print(df)
