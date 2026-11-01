# System Architecture

## High-Level Components
1. **Data Ingestion Layer**: Secure connectors to exchange WebSockets/REST, on-chain RPC, and alternative data.
2. **Processing Engine**: Normalization, feature engineering (technical indicators, order book imbalance, funding rates).
3. **Strategy Engine**: Pluggable modules per asset class.
4. **Risk Engine**: Position sizing (Kelly criterion variants, volatility targeting), stop-loss, exposure limits.
5. **Security Layer**: Cross-cutting (authN/Z, encryption, monitoring).
6. **Output**: Signals, dashboards, optional paper trading.

## Data Flow
See the mermaid diagram in README.md.

## Security Zones
- **Public Zone**: Market data (public APIs)
- **Private Zone**: Strategy parameters, API keys, historical P&L
- **Execution Zone**: Isolated for order placement (if enabled)
