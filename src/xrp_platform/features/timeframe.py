from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Iterable, List

import numpy as np

from xrp_platform.data.schemas import TimeframeCandle


class TimeframeAggregator:
    def __init__(self, base_timeframe: int = 1):
        self.base_timeframe = base_timeframe

    def aggregate(self, candles: Iterable[TimeframeCandle], target_timeframe: int) -> List[TimeframeCandle]:
        grouped: Dict[datetime, List[TimeframeCandle]] = {}
        for candle in candles:
            bucket = candle.timestamp - timedelta(
                minutes=candle.timestamp.minute % target_timeframe,
                seconds=candle.timestamp.second,
                microseconds=candle.timestamp.microsecond,
            )
            grouped.setdefault(bucket, []).append(candle)

        aggregated: List[TimeframeCandle] = []
        for bucket, group in grouped.items():
            opens = [c.open for c in group]
            highs = [c.high for c in group]
            lows = [c.low for c in group]
            closes = [c.close for c in group]
            volumes = [c.volume for c in group]
            vwap_num = sum(c.vwap * c.volume for c in group)
            vwap_den = sum(c.volume for c in group)
            aggregated.append(
                TimeframeCandle(
                    symbol=group[0].symbol,
                    timeframe_min=target_timeframe,
                    open=opens[0],
                    high=max(highs),
                    low=min(lows),
                    close=closes[-1],
                    volume=float(np.sum(volumes)),
                    vwap=float(vwap_num / vwap_den) if vwap_den else closes[-1],
                    timestamp=bucket,
                )
            )
        return sorted(aggregated, key=lambda c: c.timestamp)


__all__ = ["TimeframeAggregator"]
