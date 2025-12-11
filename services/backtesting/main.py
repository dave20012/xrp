from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from xrp_platform.data.schemas import BacktestResult, TimeframeCandle
from xrp_platform.utils.features import compute_features
from .engine import walk_forward

app = FastAPI(default_response_class=ORJSONResponse)


def _synthetic_series(symbol: str, points: int = 720) -> List[TimeframeCandle]:
    now = datetime.utcnow()
    candles: List[TimeframeCandle] = []
    price = 0.5
    for i in range(points):
        drift = 0.001 * ((i // 60) % 5)
        close = price + drift + 0.0005 * (i % 10)
        candles.append(
            TimeframeCandle(
                symbol=symbol,
                timeframe_min=1,
                open=close - 0.0005,
                high=close + 0.0008,
                low=close - 0.0009,
                close=close,
                volume=900_000 + (i % 30) * 1000,
                vwap=close,
                timestamp=now - timedelta(minutes=points - i),
            )
        )
    return candles


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/backtest/{symbol}", response_model=BacktestResult)
async def run_backtest(symbol: str) -> BacktestResult:
    series = _synthetic_series(symbol)
    features = compute_features(symbol, 1, series)
    _ = features  # features consumed implicitly inside walk_forward per window
    return walk_forward(symbol, series)


__all__ = ["app"]
