#!/usr/bin/env python3
import json
import sys

with open('validation_report.json', 'r') as f:
    data = json.load(f)

print('='*80)
print('STRATEGY VALIDATION RESULTS')
print('='*80)
print()
print(f"Total Strategies: {data['total_strategies']}")
print(f"Timestamp: {data['timestamp']}")
print()

approved = []
rejected = []

for name, strategy in data['strategies'].items():
    if strategy['overall_status'] == 'APPROVED':
        approved.append(name)
    else:
        rejected.append(name)

print(f"APPROVED: {len(approved)} strategies")
for s in approved:
    phases_passed = sum(1 for p in data['strategies'][s]['phases'] if p['status'] == 'PASSED')
    total_phases = len([p for p in data['strategies'][s]['phases'] if p['phase'] != 'phase_6_live_micro'])
    confidence = 'N/A'
    for phase in data['strategies'][s]['phases']:
        if phase['phase'] == 'phase_5_acceptance' and 'metrics' in phase:
            confidence = phase['metrics'].get('confidence_score', 'N/A')
    print(f"  [PASS] {s} ({phases_passed}/{total_phases} phases)")

print()
print(f"REJECTED: {len(rejected)} strategies")  
for s in rejected:
    phases_passed = sum(1 for p in data['strategies'][s]['phases'] if p['status'] == 'PASSED')
    total_phases = len([p for p in data['strategies'][s]['phases'] if p['phase'] != 'phase_6_live_micro'])
    print(f"  [FAIL] {s} ({phases_passed}/{total_phases} phases)")

print()
print('='*80)
print()
print('DETAILED PHASE RESULTS (Sample - First Strategy)')
print('='*80)

first_strat = list(data['strategies'].keys())[0]
strat_data = data['strategies'][first_strat]

print(f"\nStrategy: {first_strat}")
print(f"Overall Status: {strat_data['overall_status']}")
print()

for phase in strat_data['phases']:
    status_symbol = '[PASS]' if phase['status'] == 'PASSED' else '[FAIL]'
    print(f"  {status_symbol} {phase['phase']}")
    
    if 'metrics' in phase:
        m = phase['metrics']
        print(f"      Win Rate: {m.get('win_rate', 'N/A'):.1%}")
        print(f"      Sharpe: {m.get('sharpe_ratio', 'N/A'):.2f}")
        print(f"      Max DD: {m.get('max_drawdown', 'N/A'):.1%}")
        print(f"      Trades: {m.get('trades_count', 'N/A')}")
    
    if phase.get('errors'):
        print(f"      Errors: {', '.join(phase['errors'])}")
    if phase.get('warnings'):
        print(f"      Warnings: {', '.join(phase['warnings'])}")

print()
print('='*80)
print(f"Report saved to: validation_report.json")
print(f"Logs saved to: strategy_validation.log")
print('='*80)
