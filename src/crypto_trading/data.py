"""Secure data ingestion layer with validation and resilience."""
import os
import time
import hashlib
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class SecureDataClient:
    """Handles market data with security controls, rate limiting, and validation."""
    def __init__(self, use_synthetic: bool = False):
        self.api_key = os.getenv("EXCHANGE_API_KEY")  # Never hardcode; use env or secrets manager
        self.base_url = "https://api.binance.com"
        self.use_synthetic = use_synthetic
        self.last_request = 0.0
        self.min_interval = 0.2  # 5 req/s max

    def _rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

    def _validate_symbol(self, symbol: str) -> bool:
        """Basic symbol validation to prevent injection."""
        return symbol.isalnum() and len(symbol) <= 20

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        if not self._validate_symbol(symbol):
            return {"error": "invalid_symbol", "symbol": symbol}

        if self.use_synthetic:
            return {"symbol": symbol, "price": "50000.00", "synthetic": True}

        self._rate_limit()
        url = f"{self.base_url}/api/v3/ticker/price?symbol={symbol}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Basic integrity check
            if "price" not in data:
                return {"error": "malformed_response"}
            return data
        except Exception:
            return {"error": "data_unavailable", "symbol": symbol, "fallback": True}

    def get_klines(self, symbol: str, interval: str = "1h") -> list:
        if not self._validate_symbol(symbol):
            return []

        if self.use_synthetic:
            return [[0, "50000", "51000", "49000", "50500", "100"]] * 10

        self._rate_limit()
        url = f"{self.base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        try:
            resp = requests.get(url, timeout=10)
            return resp.json() if resp.ok else []
        except Exception:
            return []

    def compute_features(self, klines: list) -> Dict[str, float]:
        """Derive basic indicators from klines (closes)."""
        if not klines or len(klines) < 20:
            return {"price": 0.0, "ema_50": 0.0, "rsi": 50.0}

        closes = [float(k[4]) for k in klines[-50:]]
        price = closes[-1]
        ema_50 = sum(closes[-50:]) / len(closes[-50:]) if len(closes) >= 50 else price
        # Simplified RSI placeholder
        gains = [max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))]
        losses = [max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0
        rs = avg_gain / avg_loss if avg_loss > 0 else 100
        rsi = 100 - (100 / (1 + rs))

        return {
            "price": price,
            "ema_50": ema_50,
            "rsi": rsi,
            "volume_ratio": 1.2,  # placeholder
        }
