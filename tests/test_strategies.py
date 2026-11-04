"""Tests for enhanced strategies."""
import pytest
from src.crypto_trading.strategies import get_strategy, MajorsStrategy

def test_majors_signal_structure():
    strat = MajorsStrategy()
    data = {"price": 65000, "ema_50": 64000, "ema_200": 60000, "rsi": 55, "volume_ratio": 1.3}
    result = strat.generate_signal(data)
    assert isinstance(result, dict)
    assert result["signal"] in ["BUY", "SELL", "HOLD"]
    assert 0 <= result["confidence"] <= 1
    assert "reason" in result
    assert result["asset_class"] == "majors"

def test_get_strategy():
    strat = get_strategy("defi")
    assert strat.asset_class == "defi"
    result = strat.generate_signal({"price": 10, "tvl_change_7d": 0.1, "fee_revenue_change": 0.2, "rsi": 50})
    assert result["signal"] in ["BUY", "SELL", "HOLD"]
