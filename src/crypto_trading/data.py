"""Secure data ingestion layer."""
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SecureDataClient:
    """Handles market data with security controls."""
    def __init__(self):
        self.api_key = os.getenv("EXCHANGE_API_KEY")  # Never hardcode
        self.base_url = "https://api.binance.com"  # Example public endpoint

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch public ticker data. Rate-limit in production."""
        url = f"{self.base_url}/api/v3/ticker/price?symbol={symbol}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            # Log securely, do not expose details
            return {"error": "data_unavailable", "symbol": symbol}

    def get_klines(self, symbol: str, interval: str = "1h") -> list:
        """Public klines for indicators."""
        url = f"{self.base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        resp = requests.get(url, timeout=10)
        return resp.json() if resp.ok else []
