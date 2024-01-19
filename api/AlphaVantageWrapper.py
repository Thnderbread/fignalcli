import requests
from datetime import datetime
from urllib.parse import urljoin
from dateutil.relativedelta import relativedelta


class AlphaVantageApiWrapper:
    def __init__(self, api_key) -> None:
        self.base_url = "https://www.alphavantage.co"
        self.api_key = api_key

    def make_fx_daily_request(self, from_currency: str, to_currency: str) -> dict:
        """Contacts the Alpha Vantage api for the daily time series for the given FX currency pair.

        Args:
            from_currency (str): The currency to get the price history for, e.g. USD or JPY.
            to_currency (str): The  destination currency for the price history, e.g. USD or JPY.

            Returns:
                dict: A dictionary containing all of the price data retrieved from the api.
        """
        # ? Maybe make this a custom MissingArgumentError and display usage message when raised further up the call stack?
        if not from_currency or not to_currency:
            raise ValueError("Missing from currency or to currency.")

        if not self.validate_currency_codes([from_currency, to_currency]):
            raise ValueError("Double check your currency codes.")

        if from_currency.upper() == to_currency.upper():
            raise ValueError("Please supply differing codes.")

        endpoint = "/query"
        params = {
            "function": "FX_DAILY",
            "from_symbol": from_currency.upper(),
            "to_symbol": to_currency.upper(),
            "outputsize": "full",
            "apikey": self.api_key,
        }
        response = requests.get(urljoin(self.base_url, endpoint), params=params)
        data = response.json()

        # API always returns 200 status - check for Error Message
        # instead of relying on status codes.
        if data.get("Error Message"):
            raise requests.exceptions.HTTPError(
                "Something went wrong. Please double check your currency codes."
            )

        return data

    # TODO: It's possible that the day that matches the cutoff delta is skipped in the raw dataset, meaning the entire price_data dict would be returned
    def trim_price_data(
        self, price_data: dict, cutoff_delta=6
    ) -> dict[datetime, dict[str, str]]:
        """Trims the given price data to only include data up to six months in the past.

        Args:
            priceData (dict): The price data from the alpha vantage api converted to a dict from json.
            cutoff_delta (int): The number of months to go back for the price data. Defaults to 6 months.

        Returns:
            dict: The trimmed price data, if possible - otherwise the given dict.
        """
        # Only need to go 6 months back for the price data
        cutoff_date = datetime.now() - relativedelta(months=cutoff_delta)

        # print(stuff["Time Series FX (Daily)"]["2004-12-20"]) - yields actual data
        trimmed_data = {}
        price_data_dates = list(price_data["Time Series FX (Daily)"].keys())

        target_idx = self.find_target_index(
            cutoff_date, price_data_dates, 0, len(price_data_dates) - 1
        )

        # if target_idx is none, it indicates the data set
        # does not have up to 6 months of data.
        if target_idx > -1:
            for idx, (key, value) in enumerate(
                price_data["Time Series FX (Daily)"].items()
            ):
                trimmed_data[key] = value
                # need one past the target index for the RSI calculation
                if idx - 1 == target_idx:
                    return trimmed_data
        return price_data["Time Series FX (Daily)"]

    def find_target_index(
        self, key: datetime, keys: list[datetime], low: int, high: int
    ) -> int:
        """Binary searches the ```keys``` list for the given ```key.```

        Args:
            key (datetime): Key to search for, as a YYYY-mm-dd datetime object.
            keys (list[datetime]): A list of keys that follow the YYYY-mm-dd format.

        Raises:
            ValueError: If The keys list or key is not given.

        Returns:
            int: The index of the key or None if it's not found.
        """
        if not keys:
            return -1
        elif not key:
            raise ValueError("Missing key.")

        if low > high:
            print(
                f"key type: {type(key)} | key.date: {key.date()} | key: {key} | current keys: {list(map(lambda n: n.date(), keys))}"
            )
            return -1

        mid = low + ((high - low) // 2)
        midpoint_date = keys[mid]

        if midpoint_date.date() == key.date():
            return mid
        elif key.date() < midpoint_date.date():
            return self.find_target_index(key, keys, low, high=mid - 1)
        elif key.date() > midpoint_date.date():
            return self.find_target_index(key, keys, low=mid + 1, high=high)

    def validate_currency_codes(self, codes: list[str]) -> bool:
        """Ensure all given codes are valid.

        Returns:
            bool: True if all codes are valid, false otherwise.
        """
        return all(isinstance(code, str) and len(code) == 3 for code in codes)
