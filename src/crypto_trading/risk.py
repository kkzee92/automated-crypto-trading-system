"""Risk management engine."""
from typing import Dict

class RiskManager:
    def __init__(self, max_portfolio_risk: float = 0.02):
        self.max_portfolio_risk = max_portfolio_risk
        self.max_position_size = 0.05  # 5% of portfolio per asset

    def calculate_position_size(self, portfolio_value: float, stop_loss_pct: float, volatility: float = 0.05) -> float:
        """Simple volatility-adjusted position sizing."""
        risk_amount = portfolio_value * self.max_portfolio_risk
        size = risk_amount / (stop_loss_pct * portfolio_value) if stop_loss_pct > 0 else 0
        # Cap by volatility and max size
        size = min(size, self.max_position_size / max(volatility, 0.01))
        return max(0.0, min(size, self.max_position_size))

    def check_exposure(self, current_exposures: Dict[str, float]) -> bool:
        """Ensure no single asset exceeds limits."""
        return all(v <= self.max_position_size for v in current_exposures.values())
