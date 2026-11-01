"""Asset-class specific trading strategies."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> str:
        """Return 'BUY', 'SELL', or 'HOLD'."""
        pass

class MajorsStrategy(BaseStrategy):
    """Enhanced strategy for BTC/ETH."""
    def generate_signal(self, data: Dict[str, Any]) -> str:
        # Placeholder: implement EMA crossover, etc.
        price = data.get("price", 0)
        ema_50 = data.get("ema_50", price)
        if price > ema_50 * 1.02:
            return "BUY"
        elif price < ema_50 * 0.98:
            return "SELL"
        return "HOLD"

class DeFiStrategy(BaseStrategy):
    """For DeFi tokens with additional metrics."""
    def generate_signal(self, data: Dict[str, Any]) -> str:
        # Incorporate TVL or fee changes if available
        return "HOLD"  # Implement logic

# Registry
STRATEGIES = {
    "majors": MajorsStrategy(),
    "defi": DeFiStrategy(),
    # Add more
}
