from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData

_FALLBACK_REST_PATHS = {
    "get_exchange_info": "GET /v2/spot/market",
    "get_tick": "GET /v2/spot/ticker",
    "get_depth": "GET /v2/spot/depth",
    "get_trades": "GET /v2/spot/deals",
    "get_kline": "GET /v2/spot/kline",
    "get_account": "GET /v2/account/info",
    "get_balance": "GET /v2/assets/spot/balance",
    "make_order": "POST /v2/spot/order",
    "cancel_order": "DELETE /v2/spot/order",
    "query_order": "GET /v2/spot/order-status",
    "get_open_orders": "GET /v2/spot/pending-order",
    "get_deals": "GET /v2/spot/user-deals",
}


class CoinExExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "COINEX___SPOT"
        self.rest_url = "https://api.coinex.com"
        self.wss_url = "wss://socket.coinex.com/v2/"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1min",
            "3m": "3min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "1h": "1hour",
            "2h": "2hour",
            "4h": "4hour",
            "6h": "6hour",
            "12h": "12hour",
            "1d": "1day",
            "3d": "3day",
            "1w": "1week",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}
        self.legal_currency = ["USDT", "USD", "BTC", "ETH", "USDC"]

    def get_symbol(self, symbol: str) -> str:
        return symbol.replace("-", "")

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]


class CoinExExchangeDataSpot(CoinExExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
