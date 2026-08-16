"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.bars.bar import BarData


class CoinExBarData(BarData):
    """Class CoinExBarData"""
    def __init__(
        self,
        bar_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.bar_data: dict[str, Any] | None = (
            bar_info if has_been_json_encoded and isinstance(bar_info, dict) else None
        )
        self.open_time: int | None = None
        self.open_price: float | None = None
        self.high_price: float | None = None
        self.low_price: float | None = None
        self.close_price: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> CoinExBarData:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.bar_data = (
                json.loads(self.bar_info)
                if isinstance(self.bar_info, str)
                else self.bar_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, (dict, list)):
            data = self.bar_data
            if isinstance(data, list):
                data = {"kline": data}
            raw_kline = data.get("kline", data)
            if isinstance(raw_kline, list) and len(raw_kline) >= 5:
                kline_values: list[Any] = list(raw_kline)
                self.open_time = int(kline_values[0])
                self.open_price = float(kline_values[1])
                self.close_price = float(kline_values[2])
                self.high_price = float(kline_values[3])
                self.low_price = float(kline_values[4])
                if len(kline_values) > 5:
                    self.volume = float(kline_values[5])

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

    def get_server_time(self) -> float | int | None:
        """get_server_time method"""
        return None

    def get_local_update_time(self) -> float | int | None:
        """get_local_update_time method"""
        return self.local_update_time

    def get_open_time(self) -> int:
        """get_open_time method"""
        self.init_data()
        return self.open_time or 0

    def get_open_price(self) -> float | int:
        """get_open_price method"""
        self.init_data()
        return self.open_price or 0.0

    def get_high_price(self) -> float | int:
        """get_high_price method"""
        self.init_data()
        return self.high_price or 0.0

    def get_low_price(self) -> float | int:
        """get_low_price method"""
        self.init_data()
        return self.low_price or 0.0

    def get_close_price(self) -> float | int:
        """get_close_price method"""
        self.init_data()
        return self.close_price or 0.0

    def get_volume(self) -> float | int:
        """get_volume method"""
        self.init_data()
        return self.volume or 0.0

    def get_amount(self) -> float | int:
        """get_amount method"""
        return 0.0

    def get_close_time(self) -> float | int:
        """get_close_time method"""
        return self.get_open_time()

    def get_quote_asset_volume(self) -> float | int:
        """get_quote_asset_volume method"""
        return 0.0

    def get_base_asset_volume(self) -> float | int:
        """get_base_asset_volume method"""
        return self.get_volume()

    def get_num_trades(self) -> int:
        """get_num_trades method"""
        return 0

    def get_taker_buy_base_asset_volume(self) -> float | int:
        """get_taker_buy_base_asset_volume method"""
        return 0.0

    def get_taker_buy_quote_asset_volume(self) -> float | int:
        """get_taker_buy_quote_asset_volume method"""
        return 0.0

    def get_bar_status(self) -> bool | int:
        """get_bar_status method"""
        return True

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "open_time": self.get_open_time(),
            "open_price": self.get_open_price(),
            "high_price": self.get_high_price(),
            "low_price": self.get_low_price(),
            "close_price": self.get_close_price(),
            "volume": self.get_volume(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class CoinExRequestBarData(CoinExBarData):
    """Class CoinExRequestBarData"""
    pass


class CoinExWssBarData(CoinExBarData):
    """Class CoinExWssBarData"""
    pass


__all__ = ["CoinExBarData", "CoinExRequestBarData", "CoinExWssBarData"]
