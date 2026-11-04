"""Command-line interface for demo."""
import argparse
from .strategies import STRATEGIES, get_strategy
from .data import SecureDataClient
from .risk import RiskManager
from .security import security

def demo():
    print("=== Automated Crypto Trading System Demo (Enhanced) ===")
    client = SecureDataClient(use_synthetic=True)  # Safe default
    risk = RiskManager()
    
    # Example for BTC majors
    ticker = client.get_ticker("BTCUSDT")
    print(f"BTC Price data (synthetic): {ticker}")
    
    klines = client.get_klines("BTCUSDT")
    features = client.compute_features(klines)
    print(f"Derived features: {features}")
    
    strategy = get_strategy("majors")
    signal = strategy.generate_signal(features)
    print(f"Sample signal for majors: {signal}")
    
    # Audit the signal
    security.audit_event("signal_generated", {"asset": "BTC", "signal": signal})
    
    size = risk.calculate_position_size(
        portfolio_value=100000,
        stop_loss_pct=0.02,
        volatility=0.04,
        asset_class="majors",
        confidence=signal.get("confidence", 0.5)
    )
    print(f"Suggested position size: {size:.2%} of portfolio")
    
    # Check exposure
    exp_check = risk.check_exposure({"BTC": 0.03}, "majors")
    print(f"Exposure check: {exp_check}")
    
    print("\nSecurity note: API keys from env only. Audit log active. No secrets in code.")
    print("Synthetic mode enabled for safe demo. See docs/ for full details.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["demo"])
    args = parser.parse_args()
    if args.command == "demo":
        demo()
