"""Cyber and data security utilities for the trading system."""
import os
import hmac
import hashlib
import json
import logging
from typing import Dict, Any
from datetime import datetime
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class SecurityManager:
    """Handles encryption, audit logging, and basic anomaly detection."""
    def __init__(self):
        key = os.getenv("ENCRYPTION_KEY")
        if key:
            self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
        else:
            # Generate ephemeral for demo; in prod use KMS/Vault
            self.cipher = Fernet(Fernet.generate_key())
            logger.warning("Using ephemeral encryption key - set ENCRYPTION_KEY for persistence")

        self.audit_log: list = []

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data at rest."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()

    def audit_event(self, event_type: str, details: Dict[str, Any], user: str = "system"):
        """Immutable-style audit log entry with hash chain."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event_type,
            "user": user,
            "details": details,
        }
        # Simple hash chain
        prev_hash = self.audit_log[-1]["hash"] if self.audit_log else "0"
        entry_str = json.dumps(entry, sort_keys=True) + prev_hash
        entry["hash"] = hashlib.sha256(entry_str.encode()).hexdigest()
        self.audit_log.append(entry)
        logger.info(f"AUDIT: {event_type} - {details}")
        return entry["hash"]

    def detect_anomaly(self, trade_size: float, avg_size: float, threshold: float = 5.0) -> bool:
        """Flag unusually large trades."""
        if avg_size <= 0:
            return False
        return trade_size > avg_size * threshold

    def verify_request_signature(self, payload: str, signature: str, secret: str) -> bool:
        """HMAC verification for webhook/API integrity."""
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

# Global instance for demo
security = SecurityManager()
