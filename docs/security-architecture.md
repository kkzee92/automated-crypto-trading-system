# Cyber and Data Security Architecture

## Principles
- Zero Trust: Every request authenticated/authorized; no implicit trust.
- Least Privilege: Minimal permissions for API keys, secrets, and runtime.
- Defense in Depth: Multiple layers (network, app, data, monitoring).
- Encryption everywhere: TLS 1.3+ in transit; AES-256/Fernet at rest.
- Auditability: Hash-chained logs for all critical events.

## Key Controls Implemented
- **Secrets Management**: Environment variables only; never committed. Recommend HashiCorp Vault, AWS Secrets Manager, or GitHub Encrypted Secrets.
- **API Security**: Symbol validation against injection; rate limiting; optional HMAC request signing; IP allowlisting guidance.
- **Data Protection**: Minimal PII (market data is public); encryption helpers in `security.py`; synthetic data mode for testing (PDPA/GDPR-aligned).
- **Audit Logging**: Hash-chained immutable-style entries in SecurityManager for trades, signals, anomalies.
- **Anomaly Detection**: Trade size outliers relative to average.
- **Input Validation**: Strict symbol checks; safe parsing of external data.
- **CI Security Gates**:
  - Secret scanning (recommend gitleaks in workflow)
  - Dependency vulnerability checks (pip-audit or Dependabot)
  - Static analysis
  - No real API keys in CI (use synthetic)

## Threat Model Considerations
- API key compromise → Mitigate with rotation, scoped keys (read-only for data), withdrawal disabled, IP restrictions.
- Data poisoning of signals → Validation, multi-source confirmation, anomaly detection.
- Insider threats → Audit logs, least privilege, code review.
- Exchange API outages / rate limits → Rate limiting, fallbacks, circuit breakers in risk engine.
- Supply chain → Pinned dependencies, vulnerability scanning.

## Additional Recommendations
- Use hardware security modules (HSM) or enclaves for any signing keys in live execution.
- Implement kill switches and daily loss limits in production RiskManager.
- Monitor with structured logging + SIEM.
- Regular key rotation and penetration testing.

Code: `src/crypto_trading/security.py`, `src/crypto_trading/data.py` (validation/rate-limit), `src/crypto_trading/risk.py`.
