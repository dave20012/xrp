from __future__ import annotations

from datetime import datetime
from typing import Iterable, Tuple

import numpy as np

from xrp_platform.data.schemas import FeatureVector, TimeframeCandle


def compute_features(symbol: str, timeframe: int, candles: Iterable[TimeframeCandle]) -> FeatureVector:
    candles_list = list(candles)
    closes = np.array([c.close for c in candles_list], dtype=float)
    volumes = np.array([c.volume for c in candles_list], dtype=float)
    vwap = np.array([c.vwap for c in candles_list], dtype=float)

    trend_slope = float(np.polyfit(range(len(closes)), closes, 1)[0]) if len(closes) >= 2 else 0.0
    momentum = float(closes[-1] - closes[-2]) if len(closes) >= 2 else 0.0
    rsi = float(50 + np.clip(momentum, -5, 5) * 5)
    volatility = float(np.std(closes)) if len(closes) >= 2 else 0.0
    compression = float(1 / (1 + volatility)) if volatility else 1.0
    accumulation = float(np.sum(volumes[-3:]) / (np.mean(volumes) + 1e-6)) if len(volumes) else 0.0
    imbalance = float((closes[-1] - np.mean(closes)) / (np.std(closes) + 1e-6)) if len(closes) else 0.0

    now = max((c.timestamp for c in candles_list), default=datetime.utcnow())

    return FeatureVector(
        symbol=symbol,
        timeframe_min=timeframe,
        computed_at=now,
        technical={
            "trend_slope": trend_slope,
            "volatility_compression": compression,
            "divergence": float(closes[-1] - vwap[-1]) if len(vwap) else 0.0,
            "momentum": momentum,
            "rsi": rsi,
            "acceleration": float(momentum - (closes[-2] - closes[-3])) if len(closes) >= 3 else 0.0,
            "cluster_match": float(compression * 0.5 + trend_slope * 0.1),
            "analogue_score": float(np.tanh(trend_slope) * 50),
            "pullback_depth": float((np.max(closes) - closes[-1]) / (np.max(closes) + 1e-6)) if len(closes) else 0.0,
            "breakout_strength": float((closes[-1] - np.min(closes)) / (np.std(closes) + 1e-6)) if len(closes) else 0.0,
            "zscore": imbalance,
        },
        volume={
            "rvol": float(accumulation),
            "accumulation": float(accumulation - 1),
            "imbalance": imbalance,
        },
        order_book={
            "depth_skew": float(np.tanh(imbalance)),
            "spoof_likelihood": 0.0,
            "microprice_drift": float(trend_slope),
        },
        news={"sentiment_level": 0.0, "sentiment_velocity": 0.0, "shock": 0.0},
        onchain={
            "flow_direction": 0.0,
            "active_address_divergence": 0.0,
            "exchange_balance_delta": 0.0,
        },
        meta={
            "volatility_regime": float(volatility / (np.mean(closes) + 1e-6)) if len(closes) else 1.0,
            "trend_strength": float(np.tanh(trend_slope)),
            "noise_ratio": float(volatility / (abs(trend_slope) + 1e-6)) if trend_slope else 0.0,
        },
    )


__all__ = ["compute_features"]
