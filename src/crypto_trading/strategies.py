"""Asset-class specific trading strategies with enhanced logic."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import statistics

class BaseStrategy(ABC):
    """Abstract base for all strategies."""
    name: str = "base"
    asset_class: str = "general"

    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Return signal dict: {'signal': 'BUY'|'SELL'|'HOLD', 'confidence': float, 'reason': str, 'size_pct': float}"""
        pass

    def _safe_get(self, data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        try:
            return float(data.get(key, default))
        except (TypeError, ValueError):
            return default

class MajorsStrategy(BaseStrategy):
    """Enhanced strategy for BTC/ETH majors: trend + mean reversion hybrid."""
    name = "majors_hybrid"
    asset_class = "majors"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        ema_50 = self._safe_get(data, "ema_50", price)
        ema_200 = self._safe_get(data, "ema_200", price)
        rsi = self._safe_get(data, "rsi", 50.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        funding_rate = self._safe_get(data, "funding_rate", 0.0)

        signal = "HOLD"
        confidence = 0.3
        reason = "Neutral market conditions"
        size_pct = 0.5

        # Trend following
        if price > ema_50 > ema_200 and volume_ratio > 1.2:
            signal = "BUY"
            confidence = 0.75
            reason = "Bullish trend with volume confirmation"
            size_pct = 1.0
        elif price < ema_50 < ema_200 and volume_ratio > 1.1:
            signal = "SELL"
            confidence = 0.7
            reason = "Bearish trend confirmed"
            size_pct = 0.8
        # Mean reversion overlay
        elif rsi < 30 and price < ema_50 * 0.97:
            signal = "BUY"
            confidence = 0.65
            reason = "Oversold mean reversion"
            size_pct = 0.6
        elif rsi > 70 and price > ema_50 * 1.03:
            signal = "SELL"
            confidence = 0.6
            reason = "Overbought mean reversion"
            size_pct = 0.5

        # Funding rate adjustment
        if funding_rate > 0.01 and signal == "BUY":
            confidence *= 0.8
            reason += "; high positive funding reduces long bias"

        return {
            "signal": signal,
            "confidence": round(confidence, 2),
            "reason": reason,
            "size_pct": size_pct,
            "asset_class": self.asset_class
        }

class LargeAltsStrategy(BaseStrategy):
    """Momentum and relative strength for large alts (SOL, BNB, etc.)."""
    name = "large_alts_momentum"
    asset_class = "large_alts"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        btc_relative = self._safe_get(data, "btc_relative_strength", 1.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        macd_hist = self._safe_get(data, "macd_histogram", 0.0)

        signal = "HOLD"
        confidence = 0.4
        reason = "Awaiting momentum confirmation"
        size_pct = 0.4

        if btc_relative > 1.05 and macd_hist > 0 and volume_ratio > 1.5:
            signal = "BUY"
            confidence = 0.8
            reason = "Strong relative strength vs BTC + momentum"
            size_pct = 0.9
        elif btc_relative < 0.95 and macd_hist < 0:
            signal = "SELL"
            confidence = 0.7
            reason = "Underperforming BTC with negative momentum"
            size_pct = 0.7

        return {
            "signal": signal,
            "confidence": round(confidence, 2),
            "reason": reason,
            "size_pct": size_pct,
            "asset_class": self.asset_class
        }

class DeFiStrategy(BaseStrategy):
    """DeFi-specific with protocol metrics."""
    name = "defi_protocol_aware"
    asset_class = "defi"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        tvl_change = self._safe_get(data, "tvl_change_7d", 0.0)
        fee_change = self._safe_get(data, "fee_revenue_change", 0.0)
        rsi = self._safe_get(data, "rsi", 50.0)

        signal = "HOLD"
        confidence = 0.35
        reason = "Monitoring protocol health"
        size_pct = 0.3

        if tvl_change > 0.05 and fee_change > 0.1 and rsi < 60:
            signal = "BUY"
            confidence = 0.7
            reason = "Growing TVL and fees with non-overbought price"
            size_pct = 0.6
        elif tvl_change < -0.1 or fee_change < -0.15:
            signal = "SELL"
            confidence = 0.65
            reason = "Declining protocol metrics"
            size_pct = 0.5

        return {
            "signal": signal,
            "confidence": round(confidence, 2),
            "reason": reason,
            "size_pct": size_pct,
            "asset_class": self.asset_class
        }

class StablecoinStrategy(BaseStrategy):
    """Low-risk arb and yield signals for stables."""
    name = "stable_arb_yield"
    asset_class = "stablecoins"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        premium = self._safe_get(data, "premium_to_peg", 0.0)
        yield_diff = self._safe_get(data, "yield_diff_bps", 0.0)

        signal = "HOLD"
        confidence = 0.5
        reason = "Peg stable, monitoring yields"
        size_pct = 0.2

        if abs(premium) > 0.005:  # 0.5% depeg opportunity
            signal = "BUY" if premium < 0 else "SELL"
            confidence = 0.85
            reason = f"Arbitrage opportunity: premium {premium:.4f}"
            size_pct = 1.0
        elif yield_diff > 50:  # 50 bps better yield
            signal = "BUY"
            confidence = 0.6
            reason = "Attractive yield differential"
            size_pct = 0.4

        return {
            "signal": signal,
            "confidence": round(confidence, 2),
            "reason": reason,
            "size_pct": size_pct,
            "asset_class": self.asset_class
        }

class HighVolStrategy(BaseStrategy):
    """Strict risk controls for high-vol assets (memecoins, etc.)."""
    name = "high_vol_controlled"
    asset_class = "high_volatility"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        atr_pct = self._safe_get(data, "atr_pct", 5.0)
        volume_spike = self._safe_get(data, "volume_ratio", 1.0)

        # Always conservative
        signal = "HOLD"
        confidence = 0.2
        reason = "High volatility - waiting for extreme setup"
        size_pct = 0.1  # Max 0.1 of normal size

        if volume_spike > 3.0 and atr_pct < 8.0:  # Controlled spike
            signal = "BUY"
            confidence = 0.45
            reason = "Volume spike in moderate ATR - small position only"
            size_pct = 0.15

        return {
            "signal": signal,
            "confidence": round(confidence, 2),
            "reason": reason,
            "size_pct": size_pct,
            "asset_class": self.asset_class
        }

# Strategy registry with asset class mapping
STRATEGIES: Dict[str, BaseStrategy] = {
    "majors": MajorsStrategy(),
    "large_alts": LargeAltsStrategy(),
    "defi": DeFiStrategy(),
    "stablecoins": StablecoinStrategy(),
    "high_volatility": HighVolStrategy(),
}

def get_strategy(asset_class: str) -> BaseStrategy:
    """Retrieve strategy for given asset class."""
    return STRATEGIES.get(asset_class, MajorsStrategy())
