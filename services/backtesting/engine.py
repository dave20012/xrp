from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np

from xrp_platform.signals.composite import CompositeEngine
from xrp_platform.utils.features import compute_features
from xrp_platform.data.schemas import BacktestResult, TimeframeCandle


def walk_forward(symbol: str, candles: Iterable[TimeframeCandle], window: int = 60) -> BacktestResult:
    engine = CompositeEngine()
    equity = 1_000_000.0
    equity_curve: List[float] = [equity]
    trades = 0
    wins = 0

    candle_list = list(candles)
    for i in range(window, len(candle_list)):
        window_candles = candle_list[i - window : i]
        features = compute_features(symbol, 1, window_candles)
        signal = engine.compute(features)
        last_close = window_candles[-1].close
        if signal.composite > signal.thresholds["bullish"]:
            pnl = last_close * 0.001
            equity *= 1 + pnl
            wins += 1
            trades += 1
        elif signal.composite < signal.thresholds["bearish"]:
            pnl = -last_close * 0.001
            equity *= 1 + pnl
            trades += 1
        equity_curve.append(equity)

    returns = np.diff(equity_curve) / equity_curve[:-1]
    sharpe = float(np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(252)) if len(returns) else 0.0
    max_drawdown = float(np.max(np.maximum.accumulate(equity_curve) - equity_curve)) if equity_curve else 0.0
    expectancy = float(np.mean(returns)) if len(returns) else 0.0
    win_rate = wins / trades if trades else 0.0

    return BacktestResult(
        equity_curve=equity_curve,
        sharpe=sharpe,
        max_drawdown=max_drawdown,
        expectancy=expectancy,
        trades=trades,
        win_rate=win_rate,
        duration_days=len(equity_curve) / (60 * 24),
    )


__all__ = ["walk_forward"]
