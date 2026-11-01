import yfinance as yf
import pandas as pd
from datetime import datetime

# MARKET RESEARCH AI
# Five-Year Historical Stock Scanner

SYMBOLS = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "TCS.NS",
    "INFY.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "RELIANCE.NS",
    "BEL.NS"
]


def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def analyze_stock(symbol):

    print(f"\nAnalyzing {symbol}...")

    try:
        data = yf.download(
            symbol,
            period="5y",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if data.empty:
            print("No data available.")
            return None

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.dropna(subset=["Close"])

        data["EMA20"] = data["Close"].ewm(
            span=20, adjust=False
        ).mean()

        data["EMA50"] = data["Close"].ewm(
            span=50, adjust=False
        ).mean()

        data["RSI"] = calculate_rsi(data["Close"])

        data["Candle"] = (
            data["Close"] > data["Open"]
        ).map({
            True: "GREEN",
            False: "RED"
        })

        latest = data.iloc[-1]

        if (
            latest["Close"] > latest["EMA20"]
            and latest["EMA20"] > latest["EMA50"]
            and latest["RSI"] > 50
        ):
            signal = "BULLISH WATCH"

        elif (
            latest["Close"] < latest["EMA20"]
            and latest["EMA20"] < latest["EMA50"]
            and latest["RSI"] < 50
        ):
            signal = "BEARISH WATCH"

        else:
            signal = "NEUTRAL"

        result = {
            "Date":latest.name.strftime("%Y-%m-%d"),
            "Stock": symbol,
            "Close": round(float(latest["Close"]), 2),
            "EMA20": round(float(latest["EMA20"]), 2),
            "EMA50": round(float(latest["EMA50"]), 2),
            "RSI": round(float(latest["RSI"]), 2),
            "Last_Candle": latest["Candle"],
            "Signal": signal
        }

        print(result)

        return result

    except Exception as error:
        print(f"Error analyzing {symbol}: {error}")
        return None


def main():

    print("=" * 55)
    print("       MARKET RESEARCH AI")
    print("       FIVE YEAR STOCK SCANNER")
    print("=" * 55)

    results = []

    for symbol in SYMBOLS:

        result = analyze_stock(symbol)

        if result is not None:
            results.append(result)

    if results:

        report = pd.DataFrame(results)

        filename = "market_research_report.csv"

        report.to_csv(filename, index=False)

        print("\nREPORT SAVED:", filename)
        print("\nFINAL STOCK SUMMARY")
        print(report.to_string(index=False))

    else:
        print("No stock data available.")


if __name__ == "__main__":
    main()