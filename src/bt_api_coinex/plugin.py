from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.plugins.protocol import PluginInfo

if TYPE_CHECKING:
    from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
    from bt_api_base.registry import ExchangeRegistry

from bt_api_coinex import __version__
from bt_api_coinex.registry_registration import register_coinex


def get_plugin_info() -> PluginInfo:
    return PluginInfo(
        name="bt_api_coinex",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("COINEX___SPOT",),
        supported_asset_types=("SPOT",),
        plugin_module="bt_api_coinex.plugin",
    )


def register_plugin(
    registry: ExchangeRegistry | type[ExchangeRegistry],
    runtime_factory: type[GatewayRuntimeRegistrar],
) -> PluginInfo:
    del runtime_factory
    register_coinex(registry)
    return get_plugin_info()
