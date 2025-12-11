from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List

import numpy as np

from xrp_platform.data.schemas import CompositeSignal, FeatureVector, SignalScore
from xrp_platform.signals.modules import MODULES


class CompositeEngine:
    def __init__(self) -> None:
        self.base_weights: Dict[str, float] = {m.name: 1.0 for m in MODULES}

    def adapt_weights(self, regime: str) -> Dict[str, float]:
        weights = self.base_weights.copy()
        if regime == "high_volatility":
            weights["regime_classifier"] *= 1.5
            weights["order_book_microstructure"] *= 1.2
            weights["momentum_reversal"] *= 0.8
        elif regime == "trending":
            weights["technical_trend"] *= 1.5
            weights["volume_flow"] *= 1.2
        elif regime == "range_bound":
            weights["momentum_reversal"] *= 1.4
            weights["heuristic_swarm"] *= 1.1
        return weights

    def classify_regime(self, features: FeatureVector) -> str:
        vol_regime = features.meta.get("volatility_regime", 1.0)
        trend_strength = features.meta.get("trend_strength", 0.0)
        if vol_regime > 1.5:
            return "high_volatility"
        if trend_strength > 0.5:
            return "trending"
        return "range_bound"

    def thresholds(self) -> Dict[str, float]:
        return {"strong_sell": 20.0, "bearish": 40.0, "neutral": 60.0, "bullish": 80.0}

    def compute(self, features: FeatureVector) -> CompositeSignal:
        regime = self.classify_regime(features)
        weights = self.adapt_weights(regime)
        module_scores: List[SignalScore] = [module.score(features) for module in MODULES]

        weighted = []
        weight_sum = 0.0
        for score in module_scores:
            weight = weights.get(score.module, 1.0)
            weighted.append(score.score * weight)
            weight_sum += weight
        composite_score = float(np.sum(weighted) / weight_sum) if weight_sum else 0.0

        return CompositeSignal(
            symbol=features.symbol,
            timeframe_min=features.timeframe_min,
            computed_at=features.computed_at,
            scores=module_scores,
            composite=composite_score,
            regime=regime,
            thresholds=self.thresholds(),
        )


__all__ = ["CompositeEngine"]
