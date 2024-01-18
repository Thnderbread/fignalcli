import os
import json
import requests
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query?function=FX_DAILY"


def get_price_data(from_currency: str, to_currency: str, outfile: bool) -> dict:
    """Contacts the Alpha Vantage api for the exchange rate for the given currencies.

    Args:
        from_currency (str): The currency to get the exchange rate for, e.g. USD or JPY.
        to_currency (str): The  destination currency for the exchange rate, e.g. USD or JPY.
    """
    if not from_currency or not to_currency:
        raise ValueError("Missing from currency or to currency.")

    url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_currency}&to_symbol={to_currency}&outputsize=full&apikey={key}"
    print(url)

    dict.fromkeys()

    # TODO: error handling for bad requests - check codes for different cases (bad key, not found currencies) - (mangle the url for testing stuff)

    response = requests.get(url)
    data = response.json()

    return json.load(data)


def trim_price_data(priceData: dict) -> dict:
    raw_cutoff_date = datetime.now() - relativedelta(months=6)
    cutoff_date = raw_cutoff_date.strftime("%Y-%m-%d")

    trimmed_data = {}
    target_idx = binary_search(cutoff_date, priceData)

    if target_idx is not None:
        for idx, (key, value) in enumerate(priceData.items()):
            trimmed_data[key] = value
            # need one past the target index for the RSI calculation
            if idx - 1 == target_idx:
                return trimmed_data
    return priceData

    # if outfile:
    #     with open("forex.json", "r") as f:
    #         stuff = json.load(f)
    #         print(stuff.keys())
    #         print(type(stuff))
    #         print(stuff["Time Series FX (Daily)"]["2004-12-20"])


def binary_search(key: str, keys: list[str]) -> int:
    """Searches the ```keys``` list for the given ```key.```

    Args:
        key (str): Key to search for, as a YYYY-mm-dd string.
        keys (list[str]): A list of keys that follow the YYYY-mm-dd format.

    Raises:
        ValueError: If The keys list or key is not given.

    Returns:
        int: The index of the key or None if it's not found.
    """
    if not keys:
        raise ValueError("Missing keys list.")
    elif not key:
        raise ValueError("Missing key.")

    idx = len(keys) // 2
    m = keys[idx]
    parsed_date = parser.parse(m)

    if parsed_date == key:
        return idx
    elif parsed_date < key:
        return binary_search(key, keys[idx + 1 :])
    elif parsed_date > key:
        return binary_search(key, keys[:idx])
    else:
        return None


def extract_features(priceData: dict) -> dict:
    """Creates the features that will be passed into the ai model.

    Args:
        priceData (dict): The price data containing the high, low, open and close prices.

    Returns:
        dict: The price data with the RSI, MACD, and Moving average attached.
    """
    features = {}

    features["rsi"] = calculate_rsi(priceData)
    features["macd"] = calculate_macd(priceData)
    features["moving_average"] = calculate_moving_average(priceData)
    pass


def calculate_rsi(priceData: dict) -> int:
    """Calculates the Relative Strength Index of the given dataset.

    Args:
        priceData (dict): The price data containing the high, low, open and close prices.

    Returns:
        int: The calculated Relative Strength Index
    """
    pass


def calculate_macd(priceData: dict) -> int:
    """Calculates the Moving Average Convergence/Divergence of the given dataset.

    Args:
        priceData (dict): The price data containing the high, low, open and close prices.

    Returns:
        int: The calculated MACD value.
    """
    pass


def calculate_moving_average(priceData: dict) -> int:
    """Calculates the Exponential Moving Average based on the given dataset.

    Args:
        priceData (dict): The price data containing the high, low, open and close prices.

    Returns:
        int: The calculated EMA value.
    """
    pass


if __name__ == "__main__":
    get_price_data("USD", "JPY", True)
