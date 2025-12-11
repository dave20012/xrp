from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseModel, Field


class Settings(BaseModel):
    binance_api_key: str = Field(..., alias="BINANCE_API_KEY")
    binance_api_secret: str = Field(..., alias="BINANCE_API_SECRET")
    binance_ws_url: AnyHttpUrl = Field(..., alias="BINANCE_WS_URL")
    binance_rest_url: AnyHttpUrl = Field(..., alias="BINANCE_REST_URL")

    xrpl_rpc_url: AnyHttpUrl = Field(..., alias="XRPL_RPC_URL")
    xrpl_ws_url: AnyHttpUrl = Field(..., alias="XRPL_WS_URL")
    xrpl_data_api: AnyHttpUrl = Field(..., alias="XRPL_DATA_API")

    newsapi_key: str = Field(..., alias="NEWSAPI_KEY")
    newsapi_endpoint: AnyHttpUrl = Field(..., alias="NEWSAPI_ENDPOINT")

    btc_market_feed_url: AnyHttpUrl = Field(..., alias="BTC_MARKET_FEED_URL")
    eth_market_feed_url: AnyHttpUrl = Field(..., alias="ETH_MARKET_FEED_URL")

    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: str = Field(..., alias="REDIS_URL")

    max_position_pct: float = Field(..., alias="MAX_POSITION_PCT")
    max_drawdown_pct: float = Field(..., alias="MAX_DRAWDOWN_PCT")
    stop_multiplier: float = Field(..., alias="STOP_MULTIPLIER")
    take_profit_multiplier: float = Field(..., alias="TAKE_PROFIT_MULTIPLIER")

    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    public_api_base_url: AnyHttpUrl = Field(..., alias="PUBLIC_API_BASE_URL")

    @property
    def timeframes(self) -> List[int]:
        return [1, 5, 60, 240, 1440, 10080]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


__all__ = ["get_settings", "Settings"]
