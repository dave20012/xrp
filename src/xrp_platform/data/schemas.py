from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class OrderBookSnapshot(BaseModel):
    symbol: str
    bids: List[List[float]]
    asks: List[List[float]]
    timestamp: datetime


class Trade(BaseModel):
    symbol: str
    price: float
    size: float
    side: str
    timestamp: datetime


class TimeframeCandle(BaseModel):
    symbol: str
    timeframe_min: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float
    timestamp: datetime


class FeatureVector(BaseModel):
    symbol: str
    timeframe_min: int
    computed_at: datetime
    technical: Dict[str, float]
    volume: Dict[str, float]
    order_book: Dict[str, float]
    news: Dict[str, float]
    onchain: Dict[str, float]
    meta: Dict[str, float] = Field(default_factory=dict)


class SignalExplanation(BaseModel):
    factors: Dict[str, float]
    notes: Optional[str] = None


class SignalScore(BaseModel):
    module: str
    score: float
    explanation: SignalExplanation


class CompositeSignal(BaseModel):
    symbol: str
    timeframe_min: int
    computed_at: datetime
    scores: List[SignalScore]
    composite: float
    regime: str
    thresholds: Dict[str, float]


class ExecutionCommand(BaseModel):
    symbol: str
    side: str
    size: float
    entry: float
    stop: float
    take_profit: float
    expires_at: datetime
    risk_tags: Dict[str, float]


class BacktestResult(BaseModel):
    equity_curve: List[float]
    sharpe: float
    max_drawdown: float
    expectancy: float
    trades: int
    win_rate: float
    duration_days: float


__all__ = [
    "OrderBookSnapshot",
    "Trade",
    "TimeframeCandle",
    "FeatureVector",
    "SignalExplanation",
    "SignalScore",
    "CompositeSignal",
    "ExecutionCommand",
    "BacktestResult",
]
