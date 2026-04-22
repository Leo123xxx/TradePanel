#!/usr/bin/env python3
import re
from pathlib import Path

# Read the file
with open('strategies_structured.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Define expected sections for each strategy
required_sections = [
    'STRATEGY:',
    'ASSET:',
    'TIMEFRAME:',
    'CATEGORY:',
    'ENTRY RULES (Long)',
    'ENTRY RULES (Short)',
    'EXIT RULES',
    'PARAMETERS (AI-Tunable)',
    'REGIME CONDITIONS',
    'EXPECTED BASELINE',
    'RISK FACTORS & VALIDATION',
    'IMPLEMENTATION NOTES'
]

# Extract all strategy headers
strategies = re.findall(r'## STRATEGY #(\d+): (.+)', content)
print("="*80)
print("CONSISTENCY AUDIT - STRATEGIES STRUCTURED FILE")
print("="*80)
print(f"\nTotal Strategies Found: {len(strategies)}")
print("\nStrategy List:")
for num, name in strategies:
    print(f"  [{num}] {name}")

# Check each strategy for required sections
print("\n" + "="*80)
print("SECTION COMPLETENESS CHECK")
print("="*80)

strategy_sections = re.split(r'## STRATEGY #\d+:', content)[1:]  # Skip header

issues = []
for idx, (num, strat_name) in enumerate(strategies):
    if idx < len(strategy_sections):
        section = strategy_sections[idx]
        print(f"\nStrategy #{num}: {strat_name}")
        missing = []
        for req_section in required_sections:
            if req_section.upper() not in section.upper():
                missing.append(req_section)
                print(f"  ❌ MISSING: {req_section}")
        
        if not missing:
            print(f"  ✓ All required sections present")
        else:
            issues.append((num, strat_name, missing))

# Check parameter ranges format
print("\n" + "="*80)
print("PARAMETER RANGE FORMAT CHECK ([Min..Max])")
print("="*80)

param_tables = re.findall(r'\| Parameter \| Range \|.*?\n\|.*?\n((?:\|.*?\n)+)', content)
print(f"Found {len(param_tables)} parameter tables")

bad_ranges = []
for table_idx, table in enumerate(param_tables):
    rows = re.findall(r'\| ([^|]+) \| (\[.*?\]) \|', table)
    for param, range_val in rows:
        # Check if range follows [X..Y] format
        if not re.match(r'^\[\d+(\.\d+)?\.\.[\d\.\w]+\]$', range_val.strip()):
            bad_ranges.append((table_idx + 1, param.strip(), range_val.strip()))
            print(f"  Strategy {table_idx + 1}, Param '{param.strip()}': {range_val.strip()}")

if not bad_ranges:
    print("  ✓ All parameter ranges properly formatted")

# Check for vague language
print("\n" + "="*80)
print("CLARITY CHECK (Vague Language)")
print("="*80)

vague_terms = [
    ('maybe', 'uncertain/ambiguous'),
    ('might', 'uncertain/ambiguous'),
    ('possibly', 'uncertain/ambiguous'),
    ('somewhat', 'vague quantity'),
    ('fairly', 'vague degree'),
    ('generally', 'vague quantifier'),
    ('usually', 'vague frequency'),
    ('often', 'vague frequency'),
    ('sometimes', 'vague frequency'),
    ('roughly', 'vague number'),
    ('almost', 'uncertain threshold'),
]

vague_found = []
for term, category in vague_terms:
    matches = re.finditer(rf'\b{term}\b', content, re.IGNORECASE)
    for match in matches:
        line_num = content[:match.start()].count('\n') + 1
        vague_found.append((term, category, line_num))

if vague_found:
    print(f"Found {len(vague_found)} instances of vague language:")
    for term, category, line_num in vague_found[:15]:
        print(f"  Line ~{line_num}: '{term}' ({category})")
else:
    print("  ✓ No vague language detected")

# Check consistency of EXIT RULES format
print("\n" + "="*80)
print("EXIT RULES CONSISTENCY")
print("="*80)

exit_sections = re.findall(r'### EXIT RULES\n((?:.*?\n)+?)(?:###|---|\Z)', content)
print(f"Found {len(exit_sections)} EXIT RULES sections")

all_exits_good = True
for idx, section in enumerate(exit_sections, 1):
    has_tp = '**Take Profit:**' in section
    has_sl = '**Stop Loss:**' in section
    has_time = '**Time Exit:**' in section
    
    status = "✓" if (has_tp and has_sl and has_time) else "❌"
    if not (has_tp and has_sl and has_time):
        all_exits_good = False
    print(f"  Strategy {idx}: {status} TP={has_tp}, SL={has_sl}, TimeExit={has_time}")

# Check ENTRY RULES format consistency
print("\n" + "="*80)
print("ENTRY RULES CONSISTENCY")
print("="*80)

entry_long = len(re.findall(r'### ENTRY RULES \(Long\)', content))
entry_short = len(re.findall(r'### ENTRY RULES \(Short\)', content))
print(f"Long Entry Rules: {entry_long}")
print(f"Short Entry Rules: {entry_short}")

if entry_long == entry_short == len(strategies):
    print("  ✓ All strategies have both Long and Short entry rules")
else:
    print(f"  ❌ Mismatch: {len(strategies)} strategies but L={entry_long}, S={entry_short}")

print("\n" + "="*80)
print("SUMMARY TABLE CONSISTENCY")
print("="*80)

# Extract summary table
summary_match = re.search(r'## SUMMARY TABLE.*?\n\n(.*?)(?:\n\n---|\Z)', content, re.DOTALL)
if summary_match:
    summary_table = summary_match.group(1)
    summary_rows = re.findall(r'\| (\d+) \|', summary_table)
    print(f"Strategies in summary table: {len(summary_rows)}")
    print(f"Strategies defined: {len(strategies)}")
    if len(summary_rows) == len(strategies):
        print("  ✓ Summary table matches number of strategies")
    else:
        print(f"  ❌ Mismatch: {len(summary_rows)} in table vs {len(strategies)} defined")
else:
    print("  ❌ Summary table not found")

print("\n" + "="*80)
print("AUDIT SUMMARY")
print("="*80)
total_issues = len(issues) + len(bad_ranges) + len(vague_found) + (0 if all_exits_good else 10)
print(f"Total Issues Found: {total_issues}")
if total_issues == 0:
    print("✓ FILE IS CONSISTENT AND WELL-FORMATTED FOR AI UNDERSTANDING")
else:
    print(f"  Missing Sections: {len(issues)}")
    print(f"  Bad Parameter Ranges: {len(bad_ranges)}")
    print(f"  Vague Language: {len(vague_found)}")
    print(f"  Exit Rules Issues: {0 if all_exits_good else 'YES'}")
    print("\nRECOMMENDATION: Review and fix identified issues for optimal AI clarity")
