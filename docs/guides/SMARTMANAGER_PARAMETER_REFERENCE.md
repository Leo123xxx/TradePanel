# MT5 Smart Manager V2.2 Parameter Reference

This document provides a detailed explanation of every input parameter in the `MAW_SmartManager_V2.mq5` trade management utility. This script is responsible for managing open trades (SL/TP, Breakeven, Partial TPs, and Trailing Stops) once they are opened by the Python engine.

## 1. General Settings
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpTargetMagic` | -1 | The Magic Number to manage. `-1` means the manager will handle **ALL** trades on the current account. |
| `InpDetailedLogs` | true | If enabled, the manager will print detailed audit logs to the MT5 Experts tab for every action (BE moved, partial closed). |
| `InpTimerMs` | 500 | How often (in milliseconds) the manager scans for updates. 500ms provides high-frequency responsiveness without overloading the terminal. |

## 2. Auto SL / TP Assignment
Used if a trade is opened without a Stop Loss or Take Profit (common in manual trades or if the bot fails to set them initially).
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpAutoAssignSLTP` | true | If true, the manager will automatically calculate and set SL/TP for any trade that has them at 0. |
| `InpAssignDelaySec` | 30 | Wait time before auto-assigning. This allows the Python bot a "window" to set its own specific SL/TP before the manager takes over. |
| `InpDefaultSLATR` | 1.5 | ATR multiplier used for the automatic Stop Loss. |
| `InpDefaultTPATR` | 3.5 | ATR multiplier used for the automatic Take Profit. |

## 3. Risk Profiles (Strategy-Aware)
The manager automatically detects the "Profile" of a strategy based on keywords in the order comment.

### [DEFAULT] Profile
*Used for any strategy not matched by the Scalp, Swing, or Breakout keywords.*
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpDefBETriggerR` | 1.2 | Price must move 1.2R (120% of risk) into profit to move SL to Entry. |
| `InpDefPartial1R` | 1.5 | At 1.5R, take a partial profit. |
| `InpDefPartial1Pct` | 50.0 | Close 50% of the position at the first partial trigger. |
| `InpDefTrailTriggerR` | 2.2 | At 2.2R, start the smart trailing stop. |
| `InpDefTrailATRMult` | 3.0 | Trail the price at a distance of 3.0x ATR. |

### [SCALP] Profile
*Keywords: scalp, mql, orb*
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpScalpBEPips` | 20 | Move to BE after 20 pips of profit (hard pips for speed). |
| `InpScalpPartialPct` | 20.0 | Close 20% at the first trigger to lock in quick gains. |
| `InpScalpTrailTriggerR`| 1.5 | Start trailing much earlier (1.5R) to protect tight scalping profits. |
| `InpScalpTrailATRMult`| 1.2 | Tight trailing distance (1.2x ATR). |

### [SWING] Profile
*Keywords: swing, trend, fractal, pull, div, confluence, rsi, macd, ma*
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpSwingBETriggerR` | 1.5 | Wait for more "room" (1.5R) before moving to BE. |
| `InpSwingPartial1R` | 2.0 | First partial at 2.0R. |
| `InpSwingPartial2R` | 3.5 | Second partial at 3.5R. |
| `InpSwingTrailATRMult`| 2.5 | Wider trailing distance (2.5x ATR) to allow for market swings. |

## 4. Safety & Exit Features
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `InpWeekendClose` | false | If true, all profitable trades will be closed on Friday night. |
| `InpFridayCloseHour` | 20 | The hour (UTC) to start weekend safety operations. |
| `InpWeekendTrailMult` | 0.5 | If trading into the weekend, tighten the trailing stop by this multiplier on Friday. |

---
**Alignment Status**: Version 3.0.0 "Execution Precision"  
**Sync Date**: 2026-05-14
