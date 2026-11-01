# Cyber and Data Security Architecture

## Principles
- Zero Trust: Verify every request.
- Least Privilege.
- Defense in Depth.
- Encryption everywhere (TLS 1.3+, AES-256 at rest).

## Key Controls
- **Secrets Management**: Environment variables + optional HashiCorp Vault / AWS Secrets Manager integration.
- **API Security**: API key rotation, IP allowlisting where possible, request signing.
- **Data Protection**: PII minimization (crypto trading data is mostly public market data), encryption, audit trails.
- **Monitoring**: Anomaly detection on trade sizes, unusual API call patterns.
- **CI Security Gates**:
  - Secret scanning (gitleaks)
  - Dependency vulnerability checks
  - License compliance
  - Static analysis

## Threat Model Considerations
- API key compromise
- Data poisoning of signals
- Insider threats
- Exchange API outages / rate limits

Mitigations documented in code comments and runbooks.
