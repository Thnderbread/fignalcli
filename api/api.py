import pandas
import pandas_ta as ta


def extract_features(priceData: dict) -> dict:
    """Creates the features that will be passed into the ai model.

    Args:
        priceData (dict): The price data containing the high, low, open and close prices.

    Returns:
        dict: The price data with the RSI, MACD, and Moving average attached.
    """
    # Transpose data so that dates are columns -
    # helps w/ indexing and other time-based operations
    # also rename columns so they can be read by pandas_ta operations
    df = pandas.DataFrame(priceData).T.rename(
        columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
        }
    )

    # converting index to datetime format as it's
    # useful for time-based operations (according to chatgpt)
    df.index = pandas.to_datetime(df.index)
    features = {}

    features["rsi"] = ta.rsi(df["close"])

    features["ema12"] = df.ewm(span=12, adjust=False).mean()
    features["ema26"] = df.ewm(span=26, adjust=False).mean()

    features["macd"] = features["ema12"] - features["ema26"]
    # signal line is the 9-day period EMA of the MACD
    features["signal_line"] = features["macd"].ewm(span=9).mean()

    features["histogram"] = features["macd"] - features["signal_line"]

    return features
