"""Command-line interface for demo."""
import argparse
from .strategies import STRATEGIES
from .data import SecureDataClient
from .risk import RiskManager

def demo():
    print("=== Automated Crypto Trading System Demo ===")
    client = SecureDataClient()
    risk = RiskManager()
    
    # Example for BTC
    ticker = client.get_ticker("BTCUSDT")
    print(f"BTC Price data: {ticker}")
    
    # Simulate strategy
    strategy = STRATEGIES.get("majors")
    signal = strategy.generate_signal({"price": 65000, "ema_50": 64000})
    print(f"Sample signal for majors: {signal}")
    
    size = risk.calculate_position_size(100000, 0.02)
    print(f"Suggested position size (example): {size:.2%} of portfolio")
    
    print("\nSecurity note: API keys loaded from env only. No secrets in code.")
    print("For full strategies see docs/trading-strategies.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["demo"])
    args = parser.parse_args()
    if args.command == "demo":
        demo()
