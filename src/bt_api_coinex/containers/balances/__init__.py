"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class CoinExBalanceData(BalanceData):
    """Class CoinExBalanceData"""
    def __init__(
        self,
        balance_info: Any,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "COINEX"
        self.asset_type = asset_type
        self.balance_data: dict[str, Any] | None = balance_info if has_been_json_encoded else None
        self.currency: str | None = None
        self.available: float | None = None
        self.locked: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> CoinExBalanceData:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.balance_data = (
                json.loads(self.balance_info)
                if isinstance(self.balance_info, str)
                else self.balance_info
            )
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict):
            data = self.balance_data
            self.currency = from_dict_get_string(data, "currency")
            self.available = from_dict_get_float(data, "available", 0.0)
            self.locked = from_dict_get_float(data, "frozen", 0.0)

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        """get_all_data method"""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "currency": self.currency,
                "available": self.available,
                "locked": self.locked,
                "total": (self.available or 0.0) + (self.locked or 0.0),
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return self.exchange_name

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return float(self.local_update_time)

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return self.asset_type

    def get_server_time(self) -> float | None:
        """get_server_time method"""
        return None

    def get_currency(self) -> str | None:
        """get_currency method"""
        self.init_data()
        return self.currency

    def get_available(self) -> float | None:
        """get_available method"""
        self.init_data()
        return self.available

    def get_locked(self) -> float | None:
        """get_locked method"""
        self.init_data()
        return self.locked

    def get_total(self) -> float:
        """get_total method"""
        if self.available and self.locked:
            return self.available + self.locked
        return 0.0

    def is_zero_balance(self) -> bool:
        """is_zero_balance method"""
        return not (self.available and self.available > 0) and not (self.locked and self.locked > 0)

    def get_account_id(self) -> str | None:
        """get_account_id method"""
        return None

    def get_account_type(self) -> str | None:
        """get_account_type method"""
        return None

    def get_fee_tier(self) -> int | str | None:
        """get_fee_tier method"""
        return None

    def get_max_withdraw_amount(self) -> float | None:
        """get_max_withdraw_amount method"""
        return None

    def get_margin(self) -> float | None:
        """get_margin method"""
        return None

    def get_used_margin(self) -> float | None:
        """get_used_margin method"""
        return None

    def get_maintain_margin(self) -> float | None:
        """get_maintain_margin method"""
        return None

    def get_available_margin(self) -> float | None:
        """get_available_margin method"""
        return None

    def get_open_order_initial_margin(self) -> float | None:
        """get_open_order_initial_margin method"""
        return None

    def get_open_order_maintenance_margin(self) -> float | None:
        """get_open_order_maintenance_margin method"""
        return None

    def get_position_initial_margin(self) -> float | None:
        """get_position_initial_margin method"""
        return None

    def get_position_maintenance_margin(self) -> float | None:
        """get_position_maintenance_margin method"""
        return None

    def get_unrealized_profit(self) -> float | None:
        """get_unrealized_profit method"""
        return None

    def get_wallet_balance(self) -> float | None:
        """get_wallet_balance method"""
        return self.get_total()

    def get_equity(self) -> float | None:
        """get_equity method"""
        return self.get_total()

    def get_cross_wallet_balance(self) -> float | None:
        """get_cross_wallet_balance method"""
        return None

    def get_cross_unrealized_pnl(self) -> float | None:
        """get_cross_unrealized_pnl method"""
        return None

    def get_available_balance(self) -> float | None:
        """get_available_balance method"""
        return self.get_available()

    def get_max_withdrawal_balance(self) -> float | None:
        """get_max_withdrawal_balance method"""
        return self.get_available()


class CoinExRequestBalanceData(CoinExBalanceData):
    """Class CoinExRequestBalanceData"""
    pass


class CoinExWssBalanceData(CoinExBalanceData):
    """Class CoinExWssBalanceData"""
    pass
