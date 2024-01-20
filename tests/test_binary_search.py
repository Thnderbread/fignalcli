import pytest
from api.AlphaVantageWrapper import AlphaVantageApiWrapper


class TestBinarySearch:
    @pytest.fixture
    def api_wrapper(self):
        return AlphaVantageApiWrapper("dummy_key")

    # Returns the index of the key if it exists in the keys list.
    def test_returns_index_if_key_exists(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2021-01-03"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == 2

    # Returns None if the key is not found in the keys list.
    def test_returns_none_if_key_not_found(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2022-01-01"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == -1

    # Works correctly with a list of odd length.
    def test_works_with_odd_length_list(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2021-01-04"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == 1

    # Raises a ValueError if the keys list is empty.
    def test_raises_value_error_if_keys_list_empty(
        self, api_wrapper: AlphaVantageApiWrapper
    ):
        keys = []
        key = "2021-01-02"
        result = api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1)
        assert result == -1

    # Raises a ValueError if the key is empty.
    def test_raises_value_error_if_key_empty(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = None

        with pytest.raises(ValueError):
            api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1)

    # Works correctly with a list of even length.
    def test_works_with_even_length_list(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2021-01-02"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == 2

    def test_find_target_index_near_start(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-10": "foo",
            "2021-01-09": "foo",
            "2021-01-08": "foo",
            "2021-01-06": "foo",
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-07": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2021-01-09"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == 1

    def test_find_target_index_near_end(self, api_wrapper: AlphaVantageApiWrapper):
        d = {
            "2021-01-10": "foo",
            "2021-01-09": "foo",
            "2021-01-08": "foo",
            "2021-01-06": "foo",
            "2021-01-05": "foo",
            "2021-01-04": "foo",
            "2021-01-03": "foo",
            "2021-01-07": "foo",
            "2021-01-02": "foo",
            "2021-01-01": "foo",
        }

        keys = list(d.keys())
        key = "2021-01-02"

        assert api_wrapper.find_target_index(key, keys, low=0, high=len(keys) - 1) == 8
