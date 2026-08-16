"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.accounts.account import AccountData


class CoinExAccountData(AccountData):
    """Class CoinExAccountData"""
    def __init__(
        self,
        account_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.account_data: dict[str, Any] | str | None = (
            account_info if has_been_json_encoded else None
        )
        self.balances: list[Any] = []
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> CoinExAccountData:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.account_data = (
                json.loads(self.account_info)
                if isinstance(self.account_info, str)
                else self.account_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, dict):
            balances = self.account_data.get(
                "balance", self.account_data.get("balances", [])
            )
            if isinstance(balances, list):
                self.balances = balances

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return self.exchange_name or "COINEX"

    def get_symbol_name(self) -> str:
        """get_symbol_name method"""
        return self.symbol_name or ""

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return self.asset_type or ""

    def get_balances(self) -> list[Any]:
        """get_balances method"""
        self.init_data()
        return self.balances

    def get_server_time(self) -> int | float | None:
        """get_server_time method"""
        return None

    def get_local_update_time(self) -> int | float | None:
        """get_local_update_time method"""
        return self.local_update_time

    def get_account_id(self) -> str | None:
        """get_account_id method"""
        return None

    def get_account_type(self) -> str | None:
        """get_account_type method"""
        return None

    def get_can_deposit(self) -> bool | None:
        """get_can_deposit method"""
        return None

    def get_can_trade(self) -> bool | None:
        """get_can_trade method"""
        return None

    def get_can_withdraw(self) -> bool | None:
        """get_can_withdraw method"""
        return None

    def get_fee_tier(self) -> int | str | None:
        """get_fee_tier method"""
        return None

    def get_max_withdraw_amount(self) -> float | None:
        """get_max_withdraw_amount method"""
        return None

    def get_total_margin(self) -> float | None:
        """get_total_margin method"""
        return None

    def get_total_used_margin(self) -> float | None:
        """get_total_used_margin method"""
        return None

    def get_total_maintain_margin(self) -> float | None:
        """get_total_maintain_margin method"""
        return None

    def get_total_available_margin(self) -> float | None:
        """get_total_available_margin method"""
        return None

    def get_total_open_order_initial_margin(self) -> float | None:
        """get_total_open_order_initial_margin method"""
        return None

    def get_total_position_initial_margin(self) -> float | None:
        """get_total_position_initial_margin method"""
        return None

    def get_total_unrealized_profit(self) -> float | None:
        """get_total_unrealized_profit method"""
        return None

    def get_total_wallet_balance(self) -> float | None:
        """get_total_wallet_balance method"""
        return None

    def get_positions(self) -> list[Any]:
        """get_positions method"""
        return []

    def get_spot_maker_commission_rate(self) -> float | None:
        """get_spot_maker_commission_rate method"""
        return None

    def get_spot_taker_commission_rate(self) -> float | None:
        """get_spot_taker_commission_rate method"""
        return None

    def get_future_maker_commission_rate(self) -> float | None:
        """get_future_maker_commission_rate method"""
        return None

    def get_future_taker_commission_rate(self) -> float | None:
        """get_future_taker_commission_rate method"""
        return None

    def get_option_maker_commission_rate(self) -> float | None:
        """get_option_maker_commission_rate method"""
        return None

    def get_option_taker_commission_rate(self) -> float | None:
        """get_option_taker_commission_rate method"""
        return None

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "balances": self.balances,
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class CoinExRequestAccountData(CoinExAccountData):
    """Class CoinExRequestAccountData"""
    pass


class CoinExWssAccountData(CoinExAccountData):
    """Class CoinExWssAccountData"""
    pass


__all__ = [
    "CoinExAccountData",
    "CoinExRequestAccountData",
    "CoinExWssAccountData",
]
