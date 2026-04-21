from __future__ import annotations

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_coinex.feeds.live_coinex.request_base import CoinExRequestData


def test_coinex_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = CoinExRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="COINEX___SPOT",
    )

    monkeypatch.setattr(
        request_data,
        "http_request",
        lambda method, url, headers, body, timeout: {"code": 0, "data": []},
    )

    result = request_data.request("GET /spot/market")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"code": 0, "data": []}
