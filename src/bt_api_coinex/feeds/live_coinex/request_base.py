"""Module documentation"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed

from bt_api_coinex.exchange_data import CoinExExchangeDataSpot


class CoinExRequestData(Feed):
    """Class CoinExRequestData"""
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        """__init__ method"""
        super().__init__(data_queue, **kwargs)
        self._api_key = (
            kwargs.get("public_key")
            or kwargs.get("api_key")
            or kwargs.get("access_id")
            or ""
        )
        self._api_secret = (
            kwargs.get("private_key")
            or kwargs.get("api_secret")
            or kwargs.get("secret_key")
            or ""
        )
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.exchange_name = kwargs.get("exchange_name", "COINEX___SPOT")
        self._params = CoinExExchangeDataSpot()
        self.request_logger = self.logger
        self.async_logger = self.logger

    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_DEALS,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.GET_EXCHANGE_INFO,
        }

    def _generate_signature(self, method, request_path, body_str, timestamp):
        if not self._api_secret:
            return ""
        prepared = f"{method}{request_path}{body_str}{timestamp}"
        return (
            hmac.new(
                self._api_secret.encode("latin-1"),
                prepared.encode("latin-1"),
                hashlib.sha256,
            )
            .hexdigest()
            .lower()
        )

    def _generate_auth_headers(self, method, request_path, body_str=""):
        if not self._api_key:
            return {}
        ts = str(int(time.time() * 1000))
        sig = self._generate_signature(method, request_path, body_str, ts)
        return {
            "X-COINEX-KEY": self._api_key,
            "X-COINEX-SIGN": sig,
            "X-COINEX-TIMESTAMP": ts,
            "Content-Type": "application/json",
        }

    @staticmethod
    def _is_error(input_data: Any) -> bool:
        if not input_data:
            return True
        if isinstance(input_data, dict) and input_data.get("code") != 0:
            return True
        return False

    @staticmethod
    def _unwrap(input_data: Any) -> Any:
        if isinstance(input_data, dict) and "data" in input_data:
            return input_data["data"]
        return input_data

    def async_callback(self, future: Any) -> None:
        """async_callback method"""
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as exc:
            self.async_logger.error(f"Async callback error: {exc}")

    def push_data_to_queue(self, data: Any) -> None:
        """push_data_to_queue method"""
        if self.data_queue is not None:
            self.data_queue.put(data)

    def disconnect(self) -> None:
        """disconnect method"""
        super().disconnect()

    def request(
        self, path, params=None, body=None, extra_data=None, timeout=10, is_sign=False
    ):
        """request method"""
        if params is None:
            params = {}
        if extra_data is None:
            extra_data = {}
        method, endpoint = path.split(" ", 1)
        headers = {"Content-Type": "application/json"}

        if method in ("GET", "DELETE"):
            qs = urlencode(params) if params else ""
            request_path = f"{endpoint}?{qs}" if qs else endpoint
            url = f"{self._params.rest_url}{request_path}"
            json_body = None
            if is_sign:
                headers.update(self._generate_auth_headers(method, request_path))
        else:
            request_path = endpoint
            url = f"{self._params.rest_url}{endpoint}"
            body_str = json.dumps(body) if body else ""
            json_body = body
            if is_sign:
                headers.update(
                    self._generate_auth_headers(method, request_path, body_str)
                )

        res = self.http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    async def async_request(
        self, path, params=None, body=None, extra_data=None, timeout=5, is_sign=False
    ):
        """async_request method"""
        if params is None:
            params = {}
        if extra_data is None:
            extra_data = {}
        method, endpoint = path.split(" ", 1)
        headers = {"Content-Type": "application/json"}

        if method in ("GET", "DELETE"):
            qs = urlencode(params) if params else ""
            request_path = f"{endpoint}?{qs}" if qs else endpoint
            url = f"{self._params.rest_url}{request_path}"
            json_body = None
            if is_sign:
                headers.update(self._generate_auth_headers(method, request_path))
        else:
            request_path = endpoint
            url = f"{self._params.rest_url}{endpoint}"
            body_str = json.dumps(body) if body else ""
            json_body = body
            if is_sign:
                headers.update(
                    self._generate_auth_headers(method, request_path, body_str)
                )

        res = await self.async_http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    def _get_exchange_info(self, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_exchange_info")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_exchange_info",
            exchange_name=self.exchange_name,
            normalize_function=self._get_exchange_info_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, list):
            return data, True
        return [data], True

    def _get_tick(self, symbol, extra_data=None, **kwargs):
        coinex_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_tick")
        params = {"market": coinex_symbol}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_tick",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_tick_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        return [], False

    def _get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        coinex_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_depth")
        params = {"market": coinex_symbol, "limit": min(count, 50)}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_depth",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_depth_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        return [], False

    def _get_kline(self, symbol, period="1h", count=100, extra_data=None, **kwargs):
        coinex_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_kline")
        params = {
            "market": coinex_symbol,
            "type": self._params.get_period(period),
            "limit": count,
        }
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_kline",
            symbol_name=symbol,
            period=period,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_kline_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, list):
            return data, True
        return [], False

    def _get_trade_history(self, symbol, count=50, extra_data=None, **kwargs):
        coinex_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_trades")
        params = {"market": coinex_symbol, "limit": min(count, 50)}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_trades",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_trade_history_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_trade_history_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, list):
            return data, True
        return [], False

    def _make_order(
        self,
        symbol,
        size,
        price=None,
        order_type="buy-limit",
        extra_data=None,
        **kwargs,
    ):
        path = self._params.get_rest_path("make_order")
        coinex_symbol = self._params.get_symbol(symbol)
        parts = order_type.lower().replace("-", " ").split()
        side = parts[0] if parts else "buy"
        otype = parts[1] if len(parts) > 1 else "limit"
        body = {
            "market": coinex_symbol,
            "side": side,
            "type": otype,
            "amount": str(size),
        }
        if price is not None and otype == "limit":
            body["price"] = str(price)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="make_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._make_order_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        return [], False

    def _cancel_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("cancel_order")
        params = {}
        if order_id:
            params["id"] = str(order_id)
        if symbol:
            params["market"] = self._params.get_symbol(symbol)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="cancel_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._cancel_order_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _cancel_order_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        return [{"success": True}], True

    def _query_order(self, symbol=None, order_id=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("query_order")
        params = {}
        if order_id:
            params["id"] = str(order_id)
        if symbol:
            params["market"] = self._params.get_symbol(symbol)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="query_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._query_order_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _query_order_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        return [], False

    def _get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_open_orders")
        params = {"limit": kwargs.get("limit", 50)}
        if symbol:
            params["market"] = self._params.get_symbol(symbol)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_open_orders",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_open_orders_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_open_orders_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            orders = data.get("data", [])
            return orders, True
        if isinstance(data, list):
            return data, True
        return [], False

    def _get_deals(self, symbol=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_deals")
        params = {"limit": kwargs.get("limit", 50)}
        if symbol:
            params["market"] = self._params.get_symbol(symbol)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_deals",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_deals_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_deals_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, list):
            return data, True
        return [], False

    def _get_account(self, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_account")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_account",
            exchange_name=self.exchange_name,
            normalize_function=self._get_account_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, True
        return [data], True

    def _get_balance(self, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_balance")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_balance",
            exchange_name=self.exchange_name,
            normalize_function=self._get_balance_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data, extra_data):
        if CoinExRequestData._is_error(input_data):
            return [], False
        data = CoinExRequestData._unwrap(input_data)
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, True
        return [data], True

    def _update_extra_data(self, extra_data, **kwargs):
        if extra_data is None:
            extra_data = {}
        extra_data.update(kwargs)
        return extra_data
