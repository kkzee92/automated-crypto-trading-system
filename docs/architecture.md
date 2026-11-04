# System Architecture

## High-Level Components
1. **Secure Data Ingestion Layer** (`data.py`): Public REST connectors with rate limiting, symbol validation, synthetic fallback, basic feature engineering (EMA, RSI).
2. **Processing / Feature Engine**: Normalization and indicator derivation (extensible).
3. **Strategy Engine** (`strategies.py`): Pluggable BaseStrategy subclasses per asset class with structured signals (confidence, reason, size).
4. **Risk Engine** (`risk.py`): Volatility- and confidence-adjusted sizing, asset-class multipliers, exposure checks, drawdown halt.
5. **Security Layer** (`security.py`): Cross-cutting encryption (Fernet), hash-chained audit logging, anomaly detection, HMAC verification.
6. **Output**: CLI demo, signals, extensible to dashboards or paper trading.

## Data Flow
See the mermaid diagram in README.md. Security controls applied at every stage.

## Security Zones
- **Public Zone**: Market data (public APIs only; no keys required for basic operation)
- **Private Zone**: Strategy parameters, encrypted sensitive data, audit logs
- **Execution Zone**: Isolated (not implemented by default; would require scoped keys and additional controls)

## Extensibility
- Add new asset classes by subclassing BaseStrategy and registering.
- Integrate additional data sources (on-chain via web3.py, sentiment, etc.).
- Plug in full technical libraries (pandas-ta) for richer indicators.
- Deploy with secrets manager and monitoring for production use.
