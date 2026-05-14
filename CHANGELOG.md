# Changelog

All notable changes to the TradePanel project will be documented in this file.

## [3.0.0] - 2026-05-14
### Added
- **Directional Close Confirmation**: Mandatory requirement for candles to close in the direction of the trade (Long: Close > Open, Short: Close < Open).
- **Body Ratio Filter**: New "Conviction Gate" requiring the signal candle body to be at least 50% of the total range (ignores wicks/dojis).
- **Hardened Performance Baseline**: Added `docs/guides/STRATEGY_BASELINE_SUMMARY.md` documenting "Gold Standard" metrics for all active pairs.
- **Enhanced Execution Logging**: Signals now report detailed candle characteristics (Body%, Color, OHLC) in logs and alerts.
- **Bulk Strategy Tuning**: Successfully pushed `body_ratio_min` parameters to all 50+ strategy configurations.

### Changed
- **Strategy Registry Logic**: Unified handling of `apply_body_ratio_filter` across the strategy fleet.
- **SignalChecker Detection**: Refined to scan closed bars (`iloc[-2]`) with deeper attribute extraction for auditing.

### Fixed
- **Premature Entries**: Resolved issues where trades were entered on retracement wicks before the candle confirmed direction.
- **Signal "Flip-Flops"**: Suppressed rapid buy/sell oscillations during high-volatility news events.

## [1.1.0] - 2026-05-11
### Added
- Glassmorphic Dashboard UI v1.1.
- SWR-based API caching for high-speed frontend response.
- Server-side backtest filtering.

## [1.0.0] - 2026-05-10
- Initial Production Release.
