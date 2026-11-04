# Trading Strategies by Asset Class

Enhanced strategies with technical indicators, protocol metrics (where applicable), relative strength, and risk-aware sizing.

## Majors (BTC, ETH)
- **Hybrid Trend + Mean Reversion**: Dual EMA (50/200) crossover with volume confirmation for trend; RSI extremes (<30/>70) for mean reversion overlays.
- Funding rate awareness: reduces long bias on high positive funding.
- Confidence scoring and dynamic size_pct.
- Risk: Medium. Max size adjusted by volatility.

## Large Cap Alts (SOL, BNB, ADA, etc.)
- **Relative Strength Momentum**: Compare performance vs BTC; MACD histogram + volume spikes for entry.
- Breakouts on relative strength >1.05 with confirmation.
- Risk: Medium-High.

## DeFi Tokens (UNI, AAVE, LINK, etc.)
- **Protocol-Aware**: Incorporate TVL 7d change and fee revenue change alongside price/RSI.
- Buy on growing fundamentals with non-overbought conditions; exit on metric deterioration.
- Volatility harvesting signals.
- Risk: High.

## Stablecoins (USDT, USDC, DAI)
- **Peg Arbitrage & Yield**: Detect depeg >0.5% for arb; yield differentials >50bps for allocation signals.
- Very low directional risk.
- Risk: Low.

## High Volatility / Speculative (Memecoins, new listings)
- **Controlled Exposure**: Extreme volume spike required; max size_pct 0.15; strict ATR filters.
- Time-based and tight stop recommendations (implement in risk layer).
- Risk: Very High. Position limits enforced at 0.2x normal.

## Implementation Notes
- All strategies return structured signals: signal, confidence, reason, size_pct, asset_class.
- Hooks for backtesting and paper trading.
- Synthetic data mode for CI/safe development.
- Extend by subclassing BaseStrategy and registering in STRATEGIES.

See `src/crypto_trading/strategies.py` for code.
