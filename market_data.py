import yfinance as yf
import pandas as pd

ticker = "RELIANCE.NS"

data = yf.download(
    ticker,
    period="1y",
    interval="1d",
    progress=False
)

if data.empty:
    print("No market data received.")

else:
    data["EMA20"] = data["Close"].ewm(span=20).mean()

    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    print(data[["Close", "EMA20", "RSI"]].tail(10))

    data.to_csv("reliance_analysis.csv")

    print("Analysis saved successfully!")