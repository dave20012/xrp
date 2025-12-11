from datetime import datetime

from xrp_platform.signals.composite import CompositeEngine
from xrp_platform.data.schemas import FeatureVector


def test_composite_score_range():
    features = FeatureVector(
        symbol="XRPUSDT",
        timeframe_min=1,
        computed_at=datetime.utcnow(),
        technical={"trend_slope": 0.5, "volatility_compression": 0.8, "divergence": 0.1, "momentum": 0.2, "rsi": 55,
                   "acceleration": 0.1, "cluster_match": 0.2, "analogue_score": 0.3, "pullback_depth": 0.1,
                   "breakout_strength": 0.4, "zscore": 0.2},
        volume={"rvol": 1.2, "accumulation": 0.1, "imbalance": 0.05},
        order_book={"depth_skew": 0.1, "spoof_likelihood": 0.05, "microprice_drift": 0.2},
        news={"sentiment_level": 0.2, "sentiment_velocity": 0.05, "shock": 0.1},
        onchain={"flow_direction": 0.1, "active_address_divergence": 0.05, "exchange_balance_delta": 0.02},
        meta={"volatility_regime": 1.0, "trend_strength": 0.6, "noise_ratio": 0.2},
    )

    engine = CompositeEngine()
    signal = engine.compute(features)

    assert 0 <= signal.composite <= 100
    assert len(signal.scores) == 9
