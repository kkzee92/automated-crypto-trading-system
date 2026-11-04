"""Enhanced risk management engine with asset-class specific controls."""
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class RiskLimits:
    max_portfolio_risk: float = 0.02  # 2% per trade risk
    max_position_pct: float = 0.05    # 5% of portfolio
    max_class_exposure: float = 0.30  # 30% per asset class
    max_drawdown_halt: float = 0.15   # Halt at 15% DD

class RiskManager:
    def __init__(self, limits: RiskLimits = None):
        self.limits = limits or RiskLimits()
        self.current_drawdown = 0.0
        self.halted = False

    def calculate_position_size(
        self,
        portfolio_value: float,
        stop_loss_pct: float,
        volatility: float = 0.05,
        asset_class: str = "majors",
        confidence: float = 0.5
    ) -> float:
        """Volatility- and confidence-adjusted position sizing with class caps."""
        if self.halted or stop_loss_pct <= 0:
            return 0.0

        risk_amount = portfolio_value * self.limits.max_portfolio_risk * confidence
        raw_size = risk_amount / (stop_loss_pct * portfolio_value)

        # Volatility adjustment
        vol_adj = min(1.0, 0.05 / max(volatility, 0.01))
        size = raw_size * vol_adj

        # Asset class tighter limits
        class_multipliers = {
            "majors": 1.0,
            "large_alts": 0.8,
            "defi": 0.6,
            "stablecoins": 1.2,
            "high_volatility": 0.2,
        }
        size *= class_multipliers.get(asset_class, 0.5)

        return max(0.0, min(size, self.limits.max_position_pct))

    def check_exposure(self, current_exposures: Dict[str, float], asset_class: str = None) -> Dict[str, Any]:
        """Validate exposures against limits."""
        violations = []
        for asset, exp in current_exposures.items():
            if exp > self.limits.max_position_pct:
                violations.append(f"{asset} exceeds position limit: {exp:.2%}")

        if asset_class:
            # Placeholder for class aggregation; in full impl sum by class
            pass

        return {
            "allowed": len(violations) == 0 and not self.halted,
            "violations": violations,
            "halted": self.halted
        }

    def update_drawdown(self, current_dd: float):
        self.current_drawdown = current_dd
        if current_dd >= self.limits.max_drawdown_halt:
            self.halted = True
