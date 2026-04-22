from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orders.order import OrderData, OrderStatus
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class CoinExOrderData(OrderData):
    def __init__(
        self,
        order_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.order_data: dict[str, Any] | None = (
            order_info if has_been_json_encoded and isinstance(order_info, dict) else None
        )
        self.order_id: str | None = None
        self.order_side: str | None = None
        self.has_been_init_data = False

    def init_data(self) -> CoinExOrderData:
        if not self.has_been_json_encoded:
            self.order_data = (
                json.loads(self.order_info) if isinstance(self.order_info, str) else self.order_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.order_data, dict):
            data = self.order_data
            self.order_id = from_dict_get_string(data, "id")
            self.order_side = from_dict_get_string(data, "side")
            self.order_type = from_dict_get_string(data, "type")
            self.order_price = from_dict_get_float(data, "price")
            self.order_size = from_dict_get_float(data, "amount")
            status = from_dict_get_string(data, "status")
            if status:
                try:
                    self.order_status = OrderStatus.from_value(status)
                except ValueError:
                    self.order_status = status

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name or "COINEX"

    def get_symbol_name(self) -> str | None:
        return self.symbol_name

    def get_asset_type(self) -> str | None:
        return self.asset_type

    def get_server_time(self) -> float | None:
        return None

    def get_local_update_time(self) -> float | None:
        return self.local_update_time

    def get_trade_id(self) -> str | None:
        return None

    def get_client_order_id(self) -> str | None:
        return self.client_order_id

    def get_cum_quote(self) -> float | None:
        return self.cum_quote

    def get_executed_qty(self) -> float | None:
        return self.executed_qty

    def get_order_id(self) -> str | None:
        self.init_data()
        return self.order_id

    def get_order_size(self) -> float | None:
        self.init_data()
        return self.order_size

    def get_order_price(self) -> float | None:
        self.init_data()
        return self.order_price

    def get_reduce_only(self) -> bool | None:
        return self.reduce_only

    def get_order_side(self) -> str | None:
        self.init_data()
        return self.order_side

    def get_order_status(self) -> OrderStatus | str | None:
        self.init_data()
        return self.order_status

    def get_order_symbol_name(self) -> str | None:
        return self.symbol_name

    def get_order_time_in_force(self) -> str | None:
        return self.order_time_in_force

    def get_order_type(self) -> str | None:
        self.init_data()
        return self.order_type

    def get_order_avg_price(self) -> float | None:
        return self.order_avg_price

    def get_origin_order_type(self) -> str | None:
        return self.origin_order_type

    def get_position_side(self) -> str | None:
        return self.position_side

    def get_trailing_stop_price(self) -> float | None:
        return self.trailing_stop_price

    def get_trailing_stop_trigger_price(self) -> float | None:
        return self.trailing_stop_trigger_price

    def get_trailing_stop_callback_rate(self) -> float | None:
        return self.trailing_stop_callback_rate

    def get_trailing_stop_trigger_price_type(self) -> str | None:
        return self.trailing_stop_trigger_price_type

    def get_stop_loss_price(self) -> float | None:
        return self.stop_loss_price

    def get_stop_loss_trigger_price(self) -> float | None:
        return self.stop_loss_trigger_price

    def get_stop_loss_trigger_price_type(self) -> str | None:
        return self.stop_loss_trigger_price_type

    def get_take_profit_price(self) -> float | None:
        return self.take_profit_price

    def get_take_profit_trigger_price(self) -> float | None:
        return self.take_profit_trigger_price

    def get_take_profit_trigger_price_type(self) -> str | None:
        return self.take_profit_trigger_price_type

    def get_close_position(self) -> bool | None:
        return self.close_position

    def get_order_offset(self) -> str | None:
        return self.order_offset

    def get_order_exchange_id(self) -> str | None:
        return self.order_exchange_id

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class CoinExRequestOrderData(CoinExOrderData):
    pass


class CoinExWssOrderData(CoinExOrderData):
    pass


__all__ = ["CoinExOrderData", "CoinExRequestOrderData", "CoinExWssOrderData"]
