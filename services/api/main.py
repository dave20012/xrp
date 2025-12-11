from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from xrp_platform.data.schemas import CompositeSignal, TimeframeCandle
from xrp_platform.signals.composite import CompositeEngine
from xrp_platform.utils.features import compute_features

app = FastAPI(default_response_class=ORJSONResponse)
engine = CompositeEngine()


def _synthetic_candles(symbol: str, points: int = 60) -> List[TimeframeCandle]:
    now = datetime.utcnow()
    candles: List[TimeframeCandle] = []
    price = 0.5
    for i in range(points):
        close = price + 0.001 * (i / points)
        candles.append(
            TimeframeCandle(
                symbol=symbol,
                timeframe_min=1,
                open=close - 0.0005,
                high=close + 0.0005,
                low=close - 0.001,
                close=close,
                volume=1_000_000,
                vwap=close,
                timestamp=now - timedelta(minutes=points - i),
            )
        )
    return candles


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/signals/{symbol}", response_model=CompositeSignal)
async def signal(symbol: str) -> CompositeSignal:
    candles = _synthetic_candles(symbol)
    features = compute_features(symbol, 1, candles)
    return engine.compute(features)


__all__ = ["app"]
