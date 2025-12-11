from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict

from xrp_platform.config import get_settings
from xrp_platform.data.schemas import CompositeSignal, ExecutionCommand


class RiskEngine:
    def __init__(self) -> None:
        self.settings = get_settings()

    def size_position(self, balance: float, price: float) -> float:
        max_notional = balance * self.settings.max_position_pct / 100.0
        return max_notional / price

    def stops(self, price: float, atr: float) -> Dict[str, float]:
        stop = price - atr * self.settings.stop_multiplier
        take_profit = price + atr * self.settings.take_profit_multiplier
        return {"stop": stop, "take_profit": take_profit}


class ExecutionEngine:
    def __init__(self) -> None:
        self.risk = RiskEngine()

    def route(self, signal: CompositeSignal, balance: float, price: float, atr: float) -> ExecutionCommand | None:
        if signal.composite < signal.thresholds["bearish"]:
            side = "SELL"
        elif signal.composite > signal.thresholds["bullish"]:
            side = "BUY"
        else:
            return None

        size = self.risk.size_position(balance, price)
        stops = self.risk.stops(price, atr)
        expires_at = signal.computed_at + timedelta(minutes=signal.timeframe_min)
        return ExecutionCommand(
            symbol=signal.symbol,
            side=side,
            size=size,
            entry=price,
            stop=stops["stop"],
            take_profit=stops["take_profit"],
            expires_at=expires_at,
            risk_tags={"atr": atr, "position_pct": self.risk.settings.max_position_pct},
        )


__all__ = ["ExecutionEngine"]
