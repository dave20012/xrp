from __future__ import annotations

from math import tanh
from typing import Dict, List

import numpy as np

from xrp_platform.data.schemas import FeatureVector, SignalExplanation, SignalScore


class SignalModule:
    name: str

    def score(self, features: FeatureVector) -> SignalScore:  # pragma: no cover - interface
        raise NotImplementedError


def _bounded(value: float) -> float:
    return float(100 * tanh(value / 100))


class TechnicalTrendModule(SignalModule):
    name = "technical_trend"

    def score(self, features: FeatureVector) -> SignalScore:
        slope = features.technical.get("trend_slope", 0.0)
        compression = features.technical.get("volatility_compression", 0.0)
        divergence = features.technical.get("divergence", 0.0)
        raw = slope * 40 + compression * 10 - divergence * 15
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={
                "trend_slope": slope,
                "volatility_compression": compression,
                "divergence": -divergence,
            },
            notes="Trend slope and compression bolster the score while divergence penalizes.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class MomentumReversalModule(SignalModule):
    name = "momentum_reversal"

    def score(self, features: FeatureVector) -> SignalScore:
        momentum = features.technical.get("momentum", 0.0)
        rsi = features.technical.get("rsi", 50.0)
        accel = features.technical.get("acceleration", 0.0)
        raw = momentum * 30 + (rsi - 50) * 1.2 + accel * 25
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={"momentum": momentum, "rsi_offset": rsi - 50, "acceleration": accel},
            notes="Momentum and acceleration dominate with RSI offset acting as filter.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class VolumeFlowModule(SignalModule):
    name = "volume_flow"

    def score(self, features: FeatureVector) -> SignalScore:
        rvol = features.volume.get("rvol", 1.0)
        accumulation = features.volume.get("accumulation", 0.0)
        imbalance = features.volume.get("imbalance", 0.0)
        raw = (rvol - 1) * 20 + accumulation * 35 + imbalance * 30
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={"rvol": rvol, "accumulation": accumulation, "imbalance": imbalance},
            notes="Relative volume above 1 and accumulation push score positive; imbalance confirms.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class OrderBookMicrostructureModule(SignalModule):
    name = "order_book_microstructure"

    def score(self, features: FeatureVector) -> SignalScore:
        depth_skew = features.order_book.get("depth_skew", 0.0)
        spoof = features.order_book.get("spoof_likelihood", 0.0)
        microprice_drift = features.order_book.get("microprice_drift", 0.0)
        raw = depth_skew * 40 - spoof * 25 + microprice_drift * 35
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={
                "depth_skew": depth_skew,
                "spoof_penalty": -spoof,
                "microprice_drift": microprice_drift,
            },
            notes="Order book skew and microprice drift lead; spoof likelihood penalizes.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class NewsSentimentModule(SignalModule):
    name = "news_sentiment"

    def score(self, features: FeatureVector) -> SignalScore:
        sentiment = features.news.get("sentiment_level", 0.0)
        velocity = features.news.get("sentiment_velocity", 0.0)
        shock = features.news.get("shock", 0.0)
        raw = sentiment * 30 + velocity * 20 + shock * 40
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={"sentiment": sentiment, "velocity": velocity, "shock": shock},
            notes="Positive shocks and rising sentiment lift the module; negatives depress it.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class OnChainConfirmationModule(SignalModule):
    name = "onchain_confirmation"

    def score(self, features: FeatureVector) -> SignalScore:
        flow = features.onchain.get("flow_direction", 0.0)
        active_div = features.onchain.get("active_address_divergence", 0.0)
        exchange_delta = features.onchain.get("exchange_balance_delta", 0.0)
        raw = flow * 30 + active_div * 25 - exchange_delta * 20
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={
                "flow_direction": flow,
                "active_address_divergence": active_div,
                "exchange_balance_delta": -exchange_delta,
            },
            notes="Positive flow and address divergence confirm bias; inflows to exchanges penalize.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class RegimeClassifierModule(SignalModule):
    name = "regime_classifier"

    def score(self, features: FeatureVector) -> SignalScore:
        vol_regime = features.meta.get("volatility_regime", 0.0)
        trend_strength = features.meta.get("trend_strength", 0.0)
        noise_ratio = features.meta.get("noise_ratio", 0.0)
        raw = trend_strength * 30 - noise_ratio * 25 - abs(vol_regime - 1.0) * 20
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={
                "trend_strength": trend_strength,
                "noise_ratio": -noise_ratio,
                "volatility_regime_distance": -abs(vol_regime - 1.0),
            },
            notes="High trend strength with controlled volatility improves regime confidence.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class PatternClusterModule(SignalModule):
    name = "pattern_cluster"

    def score(self, features: FeatureVector) -> SignalScore:
        cluster_match = features.technical.get("cluster_match", 0.0)
        analogue = features.technical.get("analogue_score", 0.0)
        raw = cluster_match * 50 + analogue * 30
        score = _bounded(raw)
        explanation = SignalExplanation(
            factors={"cluster_match": cluster_match, "analogue_score": analogue},
            notes="Historical analogue and pattern match alignment drive the score.",
        )
        return SignalScore(module=self.name, score=score, explanation=explanation)


class HeuristicSwarmModule(SignalModule):
    name = "heuristic_swarm"

    def score(self, features: FeatureVector) -> SignalScore:
        bots: Dict[str, float] = {}
        bots["pullback_buy"] = features.technical.get("pullback_depth", 0.0) * -10 + features.technical.get("trend_slope", 0.0) * 25
        bots["breakout"] = features.technical.get("breakout_strength", 0.0) * 30 + features.volume.get("rvol", 1.0) * 5
        bots["mean_revert"] = -features.technical.get("zscore", 0.0) * 20 + features.volume.get("imbalance", 0.0) * -5
        swarm_score = np.tanh(np.mean(list(bots.values())) / 50) * 100 if bots else 0.0
        explanation = SignalExplanation(factors=bots, notes="Swarm aggregates lightweight heuristics across bots.")
        return SignalScore(module=self.name, score=float(swarm_score), explanation=explanation)


MODULES: List[SignalModule] = [
    TechnicalTrendModule(),
    MomentumReversalModule(),
    VolumeFlowModule(),
    OrderBookMicrostructureModule(),
    NewsSentimentModule(),
    OnChainConfirmationModule(),
    RegimeClassifierModule(),
    PatternClusterModule(),
    HeuristicSwarmModule(),
]


__all__ = ["MODULES"]
