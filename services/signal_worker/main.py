from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import List

import numpy as np

from xrp_platform.config import get_settings
from xrp_platform.data.schemas import CompositeSignal, TimeframeCandle
from xrp_platform.signals.composite import CompositeEngine
from xrp_platform.utils.features import compute_features


class SignalWorker:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.engine = CompositeEngine()

    async def fetch_candles(self, symbol: str, timeframe: int) -> List[TimeframeCandle]:
        now = datetime.utcnow()
        candles: List[TimeframeCandle] = []
        price = 0.5
        for i in range(120):
            close = price + np.sin(i / 10) * 0.01
            volume = 1_000_000 + np.cos(i / 5) * 50_000
            candles.append(
                TimeframeCandle(
                    symbol=symbol,
                    timeframe_min=1,
                    open=close - 0.002,
                    high=close + 0.002,
                    low=close - 0.003,
                    close=close,
                    volume=float(volume),
                    vwap=close,
                    timestamp=now - timedelta(minutes=120 - i),
                )
            )
        return candles

    async def compute(self, symbol: str) -> CompositeSignal:
        candles = await self.fetch_candles(symbol, 1)
        features = compute_features(symbol, 1, candles)
        return self.engine.compute(features)

    async def publish(self, signal: CompositeSignal) -> None:
        print(signal.model_dump_json())

    async def run_once(self, symbol: str) -> None:
        signal = await self.compute(symbol)
        await self.publish(signal)

    async def run(self, symbol: str) -> None:
        while True:
            await self.run_once(symbol)
            await asyncio.sleep(5)


def main() -> None:
    worker = SignalWorker()
    asyncio.run(worker.run("XRPUSDT"))


if __name__ == "__main__":
    main()
