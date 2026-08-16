"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData


class CoinExOrderBookData(OrderBookData):
    """Class CoinExOrderBookData"""
    def __init__(
        self,
        orderbook_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.order_book_data: Any = orderbook_info if has_been_json_encoded else None
        self.has_been_init_data = False

    def init_data(self) -> CoinExOrderBookData:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.order_book_data = (
                json.loads(self.order_book_info)
                if isinstance(self.order_book_info, str)
                else self.order_book_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = self.order_book_data if isinstance(self.order_book_data, dict) else {}
        self.order_book_symbol_name = self.symbol_name
        self.bid_price_list = []
        self.ask_price_list = []
        self.bid_volume_list = []
        self.ask_volume_list = []

        for item in data.get("bids", []):
            if isinstance(item, list) and len(item) >= 2:
                self.bid_price_list.append(float(item[0]))
                self.bid_volume_list.append(float(item[1]))
        for item in data.get("asks", []):
            if isinstance(item, list) and len(item) >= 2:
                self.ask_price_list.append(float(item[0]))
                self.ask_volume_list.append(float(item[1]))

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return self.exchange_name or "COINEX"

    def get_symbol_name(self) -> str | None:
        """get_symbol_name method"""
        return self.symbol_name

    def get_asset_type(self) -> str | None:
        """get_asset_type method"""
        return self.asset_type

    def get_server_time(self) -> float | None:
        """get_server_time method"""
        return None

    def get_bid_price_list(self) -> list[float] | None:
        """get_bid_price_list method"""
        self.init_data()
        return self.bid_price_list

    def get_ask_price_list(self) -> list[float] | None:
        """get_ask_price_list method"""
        self.init_data()
        return self.ask_price_list

    def get_bid_volume_list(self) -> list[float] | None:
        """get_bid_volume_list method"""
        self.init_data()
        return self.bid_volume_list

    def get_ask_volume_list(self) -> list[float] | None:
        """get_ask_volume_list method"""
        self.init_data()
        return self.ask_volume_list

    def get_bid_trade_nums(self) -> list[int] | None:
        """get_bid_trade_nums method"""
        return None

    def get_ask_trade_nums(self) -> list[int] | None:
        """get_ask_trade_nums method"""
        return None

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return float(self.local_update_time or 0.0)

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class CoinExRequestOrderBookData(CoinExOrderBookData):
    """Class CoinExRequestOrderBookData"""
    pass


class CoinExWssOrderBookData(CoinExOrderBookData):
    """Class CoinExWssOrderBookData"""
    pass


__all__ = [
    "CoinExOrderBookData",
    "CoinExRequestOrderBookData",
    "CoinExWssOrderBookData",
]
