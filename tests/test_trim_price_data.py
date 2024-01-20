import pytest

# from datetime import datetime
# from dateutil.relativedelta import relativedelta
from api.AlphaVantageWrapper import AlphaVantageApiWrapper


class TestTrimPriceData:
    @pytest.fixture
    def api_wrapper(self):
        return AlphaVantageApiWrapper("dummy_key")

    @pytest.fixture
    def raw_price_data(self):
        return {
            "Meta Data": {
                "1. Information": "Forex Daily Prices (open, high, low, close)",
                "2. From Symbol": "USD",
                "3. To Symbol": "JPY",
                "4. Output Size": "Full size",
                "5. Last Refreshed": "2024-01-18 00:15:00",
                "6. Time Zone": "UTC",
            },
            "Time Series FX (Daily)": {
                "2024-01-18": {
                    "1. open": "148.10200",
                    "2. high": "148.18000",
                    "3. low": "148.06200",
                    "4. close": "148.15800",
                },
                "2023-12-17": {
                    "1. open": "147.17300",
                    "2. high": "147.48700",
                    "3. low": "147.04400",
                    "4. close": "147.27500",
                },
                "2023-11-16": {
                    "1. open": "145.71500",
                    "2. high": "147.31100",
                    "3. low": "145.58000",
                    "4. close": "147.17200",
                },
                "2023-10-15": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
                "2023-09-14": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
                "2023-07-18": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
                "2023-07-13": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
                "2023-06-12": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
                "2023-05-11": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
            },
        }

    # Removes unnecessary keys and omits excess data
    def test_successful_dataset_trim(
        self, api_wrapper: AlphaVantageApiWrapper, raw_price_data
    ):
        trimmed_data = api_wrapper.trim_price_data(raw_price_data)

        # Unnecessary keys were removed successfully
        assert trimmed_data.get("Meta Data") is None
        assert trimmed_data.get("Time Series FX (Daily)") is None

        # Only possess six months' worth of data, and the data point after the cutoff.
        assert len(trimmed_data.keys()) == 7

    def test_unsuccessful_dataset_trim(
        self, api_wrapper: AlphaVantageApiWrapper, raw_price_data
    ):
        trimmed_data = api_wrapper.trim_price_data(raw_price_data, cutoff_delta=10)

        # Unnecessary keys were removed successfully
        assert trimmed_data.get("Meta Data") is None
        assert trimmed_data.get("Time Series FX (Daily)") is None

        # Returns the full price data, since there is not ten months' worth of data.
        assert len(trimmed_data.keys()) == 9
