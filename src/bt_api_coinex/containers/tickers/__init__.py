"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class CoinExTickerData(TickerData):
    """Class CoinExTickerData"""
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info
            if has_been_json_encoded and isinstance(ticker_info, dict)
            else None
        )
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> CoinExTickerData:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.ticker_data = (
                json.loads(self.ticker_info)
                if isinstance(self.ticker_info, str)
                else self.ticker_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, dict):
            data = self.ticker_data
            self.ticker_symbol_name = from_dict_get_string(
                data, "market", self.symbol_name
            )
            self.last_price = from_dict_get_float(data, "last", 0.0)
            self.bid_price = from_dict_get_float(data, "bid", 0.0)
            self.ask_price = from_dict_get_float(data, "ask", 0.0)
            self.high = from_dict_get_float(data, "high", 0.0)
            self.low = from_dict_get_float(data, "low", 0.0)
            self.volume = from_dict_get_float(data, "vol", 0.0)

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return self.exchange_name

    def get_symbol_name(self) -> str:
        """get_symbol_name method"""
        return self.symbol_name

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return self.asset_type

    def get_last_price(self) -> float | None:
        """get_last_price method"""
        self.init_data()
        return self.last_price

    def get_bid_price(self) -> float | None:
        """get_bid_price method"""
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        """get_ask_price method"""
        self.init_data()
        return self.ask_price

    def get_high(self) -> float | None:
        """get_high method"""
        self.init_data()
        return self.high

    def get_low(self) -> float | None:
        """get_low method"""
        self.init_data()
        return self.low

    def get_volume(self) -> float | None:
        """get_volume method"""
        self.init_data()
        return self.volume

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "ticker_symbol_name": self.ticker_symbol_name,
            "server_time": None,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "bid_volume": None,
            "ask_volume": None,
            "last_price": self.last_price,
            "last_volume": self.volume,
            "local_update_time": self.local_update_time,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return self.local_update_time

    def get_ticker_symbol_name(self) -> str | None:
        """get_ticker_symbol_name method"""
        self.init_data()
        return self.ticker_symbol_name

    def get_server_time(self) -> float | None:
        """get_server_time method"""
        return None

    def get_bid_volume(self) -> float | None:
        """get_bid_volume method"""
        return None

    def get_ask_volume(self) -> float | None:
        """get_ask_volume method"""
        return None

    def get_last_volume(self) -> float | None:
        """get_last_volume method"""
        self.init_data()
        return self.volume


__all__ = [
    "CoinExTickerData",
    "CoinExRequestTickerData",
    "CoinExWssTickerData",
]


class CoinExRequestTickerData(CoinExTickerData):
    """Class CoinExRequestTickerData"""
    pass


class CoinExWssTickerData(CoinExTickerData):
    """Class CoinExWssTickerData"""
    pass
