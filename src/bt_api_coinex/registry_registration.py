"""Module-level docstring."""
from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _coinex_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_coinex.exchange_data import CoinExExchangeDataSpot
from bt_api_coinex.feeds.live_coinex.spot import CoinExRequestDataSpot


def register_coinex(registry: ExchangeRegistry | type[ExchangeRegistry]) -> None:
    """register_coinex function"""
    registry.register_feed("COINEX___SPOT", CoinExRequestDataSpot)
    registry.register_exchange_data("COINEX___SPOT", CoinExExchangeDataSpot)
    registry.register_balance_handler("COINEX___SPOT", _coinex_balance_handler)


def register(registry: ExchangeRegistry | type[ExchangeRegistry] | None = None) -> None:
    """register function"""
    target = ExchangeRegistry if registry is None else registry
    register_coinex(target)
