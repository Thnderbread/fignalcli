import pytest
from api.AlphaVantageWrapper import AlphaVantageApiWrapper


class TestFXDailyRequest:
    @pytest.fixture
    def api_wrapper(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
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
                "2024-01-17": {
                    "1. open": "147.17300",
                    "2. high": "147.48700",
                    "3. low": "147.04400",
                    "4. close": "147.27500",
                },
                "2024-01-16": {
                    "1. open": "145.71500",
                    "2. high": "147.31100",
                    "3. low": "145.58000",
                    "4. close": "147.17200",
                },
                "2024-01-15": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
            },
        }

        mocker.patch("requests.get", return_value=mock_response)

        api_wrapper = AlphaVantageApiWrapper("dummy_key")

        return api_wrapper

    # Retrieves price data for valid currency codes.
    def test_retrieves_price_data_for_valid_currency_codes(
        self, api_wrapper: AlphaVantageApiWrapper
    ):
        expected_result = {
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
                "2024-01-17": {
                    "1. open": "147.17300",
                    "2. high": "147.48700",
                    "3. low": "147.04400",
                    "4. close": "147.27500",
                },
                "2024-01-16": {
                    "1. open": "145.71500",
                    "2. high": "147.31100",
                    "3. low": "145.58000",
                    "4. close": "147.17200",
                },
                "2024-01-15": {
                    "1. open": "144.87800",
                    "2. high": "145.94100",
                    "3. low": "144.79100",
                    "4. close": "145.71500",
                },
            },
        }
        result = api_wrapper.make_fx_daily_request("USD", "JPY")

        assert isinstance(result, dict)
        assert result == expected_result

    # Raises a ValueError if from_currency or to_currency is missing or otherwise invalid.
    @pytest.mark.parametrize(
        "from_currency, to_currency",
        [
            ("", "JPY"),
            ("USD", ""),
            ("", ""),
            (True, "USD"),
            ("US", "EU"),
            ("JPY", "JPY"),
        ],
    )
    def test_raises_value_error_if_currency_missing(
        self, api_wrapper: AlphaVantageApiWrapper, from_currency, to_currency
    ):
        with pytest.raises(ValueError) as e:
            api_wrapper.make_fx_daily_request(from_currency, to_currency)

        assert (
            str(e.value) == "Double check your currency codes."
            or "Missing from currency or to currency."
            or "Please supply differing codes."
        )
