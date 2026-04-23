from __future__ import annotations

from typing import Any

from bt_api_coinex.feeds.live_coinex.request_base import CoinExRequestData


class CoinExRequestDataSpot(CoinExRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        kwargs.setdefault("exchange_name", "COINEX___SPOT")
        kwargs.setdefault("asset_type", "SPOT")
        super().__init__(data_queue, **kwargs)

    def get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    get_ticker = get_tick
    async_get_ticker = async_get_tick

    def get_depth(
        self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(
        self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_kline(
        self,
        symbol: Any,
        period: str = "1h",
        count: int = 100,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path, params, extra_data = self._get_kline(
            symbol, period, count, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self,
        symbol: Any,
        period: Any = "1h",
        count: int = 100,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path, params, extra_data = self._get_kline(
            symbol, period, count, extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_trade_history(
        self, symbol: Any, count: int = 50, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_trade_history(
            symbol, count, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_trade_history(
        self, symbol: Any, count: int = 50, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_trade_history(
            symbol, count, extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    get_trades = get_trade_history
    async_get_trades = async_get_trade_history

    def make_order(
        self,
        symbol: str,
        volume: float,
        price: float,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        del post_only, client_order_id
        side = "buy" if offset.lower() in {"open", "buy"} else "sell"
        normalized_order_type = f"{side}-{order_type}"
        path, body, extra_data = self._make_order(
            symbol, volume, price, normalized_order_type, extra_data, **kwargs
        )
        return self.request(path, body=body, extra_data=extra_data, is_sign=True)

    def async_make_order(
        self,
        symbol: Any,
        volume: Any,
        price: Any,
        order_type: Any,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        del post_only, client_order_id
        side = "buy" if str(offset).lower() in {"open", "buy"} else "sell"
        normalized_order_type = f"{side}-{order_type}"
        path, body, extra_data = self._make_order(
            symbol, volume, price, normalized_order_type, extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, body=body, extra_data=extra_data, is_sign=True),
            callback=self.async_callback,
        )

    def cancel_order(
        self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._cancel_order(
            symbol, order_id, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_cancel_order(
        self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._cancel_order(
            symbol, order_id, extra_data, **kwargs
        )
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )

    def query_order(
        self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._query_order(
            symbol, order_id, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_query_order(
        self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._query_order(
            symbol, order_id, extra_data, **kwargs
        )
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )

    def get_open_orders(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_get_open_orders(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_open_orders(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )

    def get_deals(
        self,
        symbol: Any,
        count: int = 100,
        start_time: Any = None,
        end_time: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        del start_time, end_time
        path, params, extra_data = self._get_deals(
            symbol, extra_data, limit=count, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_get_deals(
        self,
        symbol: Any,
        count: int = 100,
        start_time: Any = None,
        end_time: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        del start_time, end_time
        path, params, extra_data = self._get_deals(
            symbol, extra_data, limit=count, **kwargs
        )
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )

    def get_account(self, symbol: Any = "ALL", extra_data: Any = None, **kwargs: Any):
        del symbol
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_get_account(
        self, symbol: Any = "ALL", extra_data: Any = None, **kwargs: Any
    ):
        del symbol
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )

    def get_balance(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        del symbol
        path, params, extra_data = self._get_balance(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def async_get_balance(
        self, symbol: Any = None, extra_data: Any = None, **kwargs: Any
    ):
        del symbol
        path, params, extra_data = self._get_balance(extra_data, **kwargs)
        self.submit(
            self.async_request(
                path, params=params, extra_data=extra_data, is_sign=True
            ),
            callback=self.async_callback,
        )
