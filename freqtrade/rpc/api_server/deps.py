from typing import Any, Dict, Iterator, Optional

from fastapi import Depends

from freqtrade.enums import RunMode
from freqtrade.persistence import Trade
from freqtrade.rpc.rpc import RPC, RPCException

from .webserver import ApiServer


def get_rpc_optional() -> Optional[RPC]:
    return ApiServer._rpc if ApiServer._has_rpc else None


def get_rpc() -> Optional[Iterator[RPC]]:
    if not (_rpc := get_rpc_optional()):
        raise RPCException('Bot is not in the correct state')
    Trade.rollback()
    yield _rpc
    Trade.rollback()


def get_config() -> Dict[str, Any]:
    return ApiServer._config


def get_api_config() -> Dict[str, Any]:
    return ApiServer._config['api_server']


def get_exchange(config=Depends(get_config)):
    if not ApiServer._exchange:
        from freqtrade.resolvers import ExchangeResolver
        ApiServer._exchange = ExchangeResolver.load_exchange(
            config['exchange']['name'], config, load_leverage_tiers=False)
    return ApiServer._exchange


def get_message_stream():
    return ApiServer._message_stream


def is_webserver_mode(config=Depends(get_config)):
    if config['runmode'] != RunMode.WEBSERVER:
        raise RPCException('Bot is not in the correct state')
    return None
