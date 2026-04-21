"""Tests for CoinexExchangeData container."""

from __future__ import annotations

from bt_api_coinex.exchange_data import CoinExExchangeData


class TestCoinExExchangeData:
    """Tests for CoinExExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = CoinExExchangeData()

        assert exchange.exchange_name == "COINEX___SPOT"
