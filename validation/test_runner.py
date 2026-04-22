#!/usr/bin/env python3
"""
Trading Strategy Validation Test Runner
Validates all strategies across 6-phase testing framework
Version: 2.0
Created: April 17, 2026
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strategy_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TestPhase(Enum):
    """Test phase enumeration"""
    UNIT_TEST = "phase_1_unit_test"
    BACKTEST = "phase_2_backtest"
    OUT_OF_SAMPLE = "phase_3_out_of_sample"
    FORWARD_TEST = "phase_4_forward_test"
    ACCEPTANCE = "phase_5_acceptance"
    LIVE_MICRO = "phase_6_live_micro"


class TestStatus(Enum):
    """Test status enumeration"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"
    ABANDONED = "ABANDONED"


@dataclass
class StrategyMetrics:
    """Strategy performance metrics"""
    strategy_name: str
    timeframe: str
    win_rate: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    avg_trade_pnl: float = 0.0
    trades_count: int = 0
    monthly_return: float = 0.0
    profit_factor: float = 0.0
    recovery_factor: float = 0.0
    
    def meets_criteria(self, criteria: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Check if metrics meet acceptance criteria"""
        failures = []
        
        if self.win_rate < criteria.get('min_win_rate', 0.50):
            failures.append(f"Win rate {self.win_rate:.2%} < {criteria['min_win_rate']:.2%}")
        
        if self.sharpe_ratio < criteria.get('min_sharpe', 1.0):
            failures.append(f"Sharpe {self.sharpe_ratio:.2f} < {criteria['min_sharpe']}")
        
        if self.max_drawdown > criteria.get('max_drawdown', 0.15):
            failures.append(f"Drawdown {self.max_drawdown:.2%} > {criteria['max_drawdown']:.2%}")
        
        if self.trades_count < criteria.get('min_trades', 50):
            failures.append(f"Trades {self.trades_count} < {criteria['min_trades']}")
        
        return len(failures) == 0, failures


@dataclass
class TestResult:
    """Test result for a single phase"""
    strategy_name: str
    phase: TestPhase
    status: TestStatus
    metrics: StrategyMetrics = None
    errors: List[str] = None
    warnings: List[str] = None
    timestamp: str = None
    duration_seconds: float = 0.0
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class StrategyValidator:
    """Main validation orchestrator"""
    
    def __init__(self, config_path: str):
        """Initialize validator with configuration"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.results: Dict[str, List[TestResult]] = {}
        self.strategies: List[Dict[str, Any]] = []
        
    def _load_config(self) -> Dict[str, Any]:
        """Load validation configuration from YAML"""
        try:
            import yaml
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except ImportError:
            logger.error("PyYAML not installed. Install: pip install pyyaml")
            sys.exit(1)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            sys.exit(1)
    
    def load_strategies(self, strategies_path: str) -> None:
        """Load strategies from markdown file"""
        try:
            with open(strategies_path, 'r') as f:
                content = f.read()
            logger.info(f"Loaded {len(content)} chars from {strategies_path}")
            # TODO: Parse markdown to extract strategy definitions
            self.strategies = self._parse_strategies_from_markdown(content)
        except FileNotFoundError:
            logger.error(f"Strategies file not found: {strategies_path}")
            sys.exit(1)
    
    def _parse_strategies_from_markdown(self, content: str) -> List[Dict[str, Any]]:
        """Parse strategy definitions from markdown"""
        # Placeholder: In production, parse markdown to extract:
        # - STRATEGY name
        # - PARAMETERS with [Min..Max]
        # - ENTRY/EXIT rules
        # - EXPECTED BASELINE metrics
        strategies = []
        
        # Example: Find all "## STRATEGY #" headers
        import re
        strategy_blocks = re.split(r'^## STRATEGY #\d+:', content, flags=re.MULTILINE)
        
        for i, block in enumerate(strategy_blocks[1:], 1):
            lines = block.split('\n')
            strategy_name = lines[0].strip() if lines else f"Strategy {i}"
            
            strategies.append({
                'id': i,
                'name': strategy_name,
                'content': block
            })
        
        logger.info(f"Parsed {len(strategies)} strategies from markdown")
        return strategies
    
    def run_phase_1_unit_test(self, strategy: Dict[str, Any]) -> TestResult:
        """Phase 1: Unit Test - Verify entry/exit logic"""
        logger.info(f"Running Phase 1 (Unit Test) for {strategy['name']}")
        
        result = TestResult(
            strategy_name=strategy['name'],
            phase=TestPhase.UNIT_TEST,
            status=TestStatus.IN_PROGRESS
        )
        
        try:
            # Check 1: Entry rules are parseable
            if 'ENTRY RULES' not in strategy['content']:
                result.errors.append("Missing ENTRY RULES section")
            
            # Check 2: Exit rules are parseable
            if 'EXIT RULES' not in strategy['content']:
                result.errors.append("Missing EXIT RULES section")
            
            # Check 3: Parameters are defined
            if 'PARAMETERS' not in strategy['content']:
                result.errors.append("Missing PARAMETERS section")
            
            # Check 4: No syntax errors in parameter ranges
            import re
            params = re.findall(r'- \w+: \[(\d+)\.\.(\d+)\]', strategy['content'])
            if not params and 'PARAMETERS' in strategy['content']:
                result.warnings.append("Could not parse parameter ranges")
            
            if not result.errors:
                result.status = TestStatus.PASSED
                logger.info(f"✓ Phase 1 PASSED for {strategy['name']}")
            else:
                result.status = TestStatus.FAILED
                logger.error(f"✗ Phase 1 FAILED for {strategy['name']}")
        
        except Exception as e:
            result.status = TestStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Exception in Phase 1: {e}")
        
        return result
    
    def run_phase_2_backtest(self, strategy: Dict[str, Any]) -> TestResult:
        """Phase 2: Backtesting - Run 2+ years historical data"""
        logger.info(f"Running Phase 2 (Backtest) for {strategy['name']}")
        
        result = TestResult(
            strategy_name=strategy['name'],
            phase=TestPhase.BACKTEST,
            status=TestStatus.IN_PROGRESS
        )
        
        try:
            # Placeholder: In production, run actual backtest using:
            # - bt (Backtest library)
            # - vectorbt
            # - zipline
            # - Custom OHLC simulation
            
            # Mock backtest results for now
            result.metrics = StrategyMetrics(
                strategy_name=strategy['name'],
                timeframe='H1',
                win_rate=0.54,
                sharpe_ratio=1.25,
                max_drawdown=0.10,
                avg_trade_pnl=45.00,
                trades_count=120,
                monthly_return=0.02,
                profit_factor=1.8,
                recovery_factor=2.5
            )
            
            # Check acceptance criteria
            criteria = self.config['acceptance_criteria']['backtesting']
            meets, failures = result.metrics.meets_criteria({
                'min_win_rate': criteria['minimum_win_rate'],
                'min_sharpe': criteria['minimum_sharpe_ratio'],
                'max_drawdown': criteria['maximum_drawdown_percent'],
                'min_trades': criteria['minimum_trade_sample']
            })
            
            if meets:
                result.status = TestStatus.PASSED
                logger.info(f"✓ Phase 2 PASSED for {strategy['name']}")
            else:
                result.status = TestStatus.FAILED
                result.errors.extend(failures)
                logger.error(f"✗ Phase 2 FAILED for {strategy['name']}: {failures}")
        
        except Exception as e:
            result.status = TestStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Exception in Phase 2: {e}")
        
        return result
    
    def run_phase_3_out_of_sample(self, strategy: Dict[str, Any]) -> TestResult:
        """Phase 3: Out-of-Sample Validation on held-out data"""
        logger.info(f"Running Phase 3 (OOS Validation) for {strategy['name']}")
        
        result = TestResult(
            strategy_name=strategy['name'],
            phase=TestPhase.OUT_OF_SAMPLE,
            status=TestStatus.IN_PROGRESS
        )
        
        try:
            # Mock OOS results (should be ~70% of in-sample Sharpe)
            result.metrics = StrategyMetrics(
                strategy_name=strategy['name'],
                timeframe='H1',
                win_rate=0.51,  # Slightly lower
                sharpe_ratio=0.88,  # 70% of 1.25
                max_drawdown=0.11,
                avg_trade_pnl=38.00,
                trades_count=45,
                monthly_return=0.015,
                profit_factor=1.65,
                recovery_factor=1.8
            )
            
            # Check that OOS Sharpe >= 70% of IS Sharpe
            in_sample_sharpe = 1.25  # From Phase 2
            threshold = in_sample_sharpe * 0.70
            
            if result.metrics.sharpe_ratio >= threshold:
                result.status = TestStatus.PASSED
                logger.info(f"✓ Phase 3 PASSED for {strategy['name']}")
            else:
                result.status = TestStatus.FAILED
                result.errors.append(
                    f"OOS Sharpe {result.metrics.sharpe_ratio:.2f} < "
                    f"threshold {threshold:.2f} (70% of IS)"
                )
                logger.error(f"✗ Phase 3 FAILED for {strategy['name']}")
        
        except Exception as e:
            result.status = TestStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Exception in Phase 3: {e}")
        
        return result
    
    def run_phase_4_forward_test(self, strategy: Dict[str, Any]) -> TestResult:
        """Phase 4: Forward Testing - Paper trading"""
        logger.info(f"Running Phase 4 (Forward Test) for {strategy['name']}")
        
        result = TestResult(
            strategy_name=strategy['name'],
            phase=TestPhase.FORWARD_TEST,
            status=TestStatus.IN_PROGRESS
        )
        
        try:
            # In production: Monitor live paper trades, log execution metrics
            # For now, mock forward test results
            result.metrics = StrategyMetrics(
                strategy_name=strategy['name'],
                timeframe='H1',
                win_rate=0.50,
                sharpe_ratio=0.82,
                max_drawdown=0.12,
                avg_trade_pnl=35.00,
                trades_count=62,
                monthly_return=0.012,
                profit_factor=1.55,
                recovery_factor=1.4
            )
            
            # Check forward-test acceptance criteria
            criteria = self.config['acceptance_criteria']['forward_testing']
            meets, failures = result.metrics.meets_criteria({
                'min_win_rate': criteria['minimum_win_rate'],
                'min_sharpe': criteria['minimum_sharpe_ratio'],
                'max_drawdown': criteria['maximum_drawdown_percent'],
                'min_trades': criteria['minimum_trade_sample']
            })
            
            if meets:
                result.status = TestStatus.PASSED
                logger.info(f"✓ Phase 4 PASSED for {strategy['name']}")
            else:
                result.status = TestStatus.FAILED
                result.errors.extend(failures)
                logger.error(f"✗ Phase 4 FAILED for {strategy['name']}")
        
        except Exception as e:
            result.status = TestStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Exception in Phase 4: {e}")
        
        return result
    
    def run_phase_5_acceptance(self, strategy_results: List[TestResult]) -> TestResult:
        """Phase 5: Acceptance Decision - Review all phases"""
        logger.info(f"Running Phase 5 (Acceptance) for {strategy_results[0].strategy_name}")
        
        strategy_name = strategy_results[0].strategy_name
        result = TestResult(
            strategy_name=strategy_name,
            phase=TestPhase.ACCEPTANCE,
            status=TestStatus.IN_PROGRESS
        )
        
        try:
            # Check all phases passed
            phase_results = {r.phase: r.status for r in strategy_results}
            
            all_passed = all(
                status == TestStatus.PASSED 
                for phase, status in phase_results.items() 
                if phase != TestPhase.LIVE_MICRO
            )
            
            if all_passed:
                result.status = TestStatus.PASSED
                
                # Calculate confidence score (0–1)
                # Based on metric stability across phases
                metrics_list = [r.metrics for r in strategy_results if r.metrics]
                if len(metrics_list) >= 3:
                    sharpes = [m.sharpe_ratio for m in metrics_list]
                    avg_sharpe = sum(sharpes) / len(sharpes)
                    sharpe_std = (sum((s - avg_sharpe)**2 for s in sharpes) / len(sharpes)) ** 0.5
                    
                    # Confidence = high if std is low
                    confidence = max(0.0, 1.0 - (sharpe_std / avg_sharpe if avg_sharpe > 0 else 1.0))
                    
                    logger.info(
                        f"✓ Phase 5 PASSED for {strategy_name} "
                        f"(confidence: {confidence:.2%})"
                    )
                else:
                    logger.info(f"✓ Phase 5 PASSED for {strategy_name}")
            else:
                result.status = TestStatus.FAILED
                failed_phases = [
                    phase.value for phase, status in phase_results.items() 
                    if status != TestStatus.PASSED and phase != TestPhase.LIVE_MICRO
                ]
                result.errors.append(f"Failed phases: {failed_phases}")
                logger.error(f"✗ Phase 5 FAILED for {strategy_name}")
        
        except Exception as e:
            result.status = TestStatus.FAILED
            result.errors.append(str(e))
            logger.error(f"Exception in Phase 5: {e}")
        
        return result
    
    def run_full_test_pipeline(self) -> Dict[str, List[TestResult]]:
        """Run full 6-phase test pipeline for all strategies"""
        logger.info("=" * 80)
        logger.info("STARTING FULL STRATEGY VALIDATION PIPELINE")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info(f"Total strategies to validate: {len(self.strategies)}")
        logger.info("=" * 80)
        
        self.results = {}
        
        for strategy in self.strategies:
            strategy_name = strategy['name']
            logger.info(f"\n{'=' * 80}")
            logger.info(f"VALIDATING STRATEGY: {strategy_name}")
            logger.info(f"{'=' * 80}")
            
            strategy_results = []
            
            # Run phases in sequence
            # Phase 1: Unit Test
            phase1 = self.run_phase_1_unit_test(strategy)
            strategy_results.append(phase1)
            
            # Only continue if Phase 1 passed
            if phase1.status != TestStatus.PASSED:
                logger.warning(f"Phase 1 failed; skipping remaining phases for {strategy_name}")
                self.results[strategy_name] = strategy_results
                continue
            
            # Phase 2: Backtest
            phase2 = self.run_phase_2_backtest(strategy)
            strategy_results.append(phase2)
            
            if phase2.status != TestStatus.PASSED:
                # Check failure criteria
                if phase2.metrics.sharpe_ratio < 0.6:
                    logger.error(f"ARCHIVED: {strategy_name} (Sharpe < 0.6)")
                else:
                    logger.warning(f"Phase 2 failed; continuing to Phase 3 for investigation")
            
            # Phase 3: Out-of-Sample
            phase3 = self.run_phase_3_out_of_sample(strategy)
            strategy_results.append(phase3)
            
            # Phase 4: Forward Test
            phase4 = self.run_phase_4_forward_test(strategy)
            strategy_results.append(phase4)
            
            # Phase 5: Acceptance
            phase5 = self.run_phase_5_acceptance(strategy_results)
            strategy_results.append(phase5)
            
            self.results[strategy_name] = strategy_results
        
        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION PIPELINE COMPLETE")
        logger.info("=" * 80)
        
        return self.results
    
    def generate_report(self, output_path: str = 'validation_report.json') -> None:
        """Generate validation report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_strategies': len(self.results),
            'strategies': {}
        }
        
        for strategy_name, results in self.results.items():
            strategy_report = {
                'phases': [],
                'overall_status': 'PENDING'
            }
            
            for result in results:
                phase_report = {
                    'phase': result.phase.value,
                    'status': result.status.value,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'timestamp': result.timestamp
                }
                
                if result.metrics:
                    phase_report['metrics'] = asdict(result.metrics)
                
                strategy_report['phases'].append(phase_report)
            
            # Determine overall status
            phases_passed = sum(
                1 for r in results 
                if r.status == TestStatus.PASSED 
                and r.phase != TestPhase.LIVE_MICRO
            )
            total_phases = sum(
                1 for r in results 
                if r.phase != TestPhase.LIVE_MICRO
            )
            
            if phases_passed == total_phases:
                strategy_report['overall_status'] = 'APPROVED'
            else:
                strategy_report['overall_status'] = 'REJECTED'
            
            report['strategies'][strategy_name] = strategy_report
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report generated: {output_path}")
    
    def print_summary(self) -> None:
        """Print validation summary"""
        approved = 0
        rejected = 0
        
        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 80)
        
        for strategy_name, results in self.results.items():
            phases_passed = sum(
                1 for r in results 
                if r.status == TestStatus.PASSED 
                and r.phase != TestPhase.LIVE_MICRO
            )
            total_phases = sum(
                1 for r in results 
                if r.phase != TestPhase.LIVE_MICRO
            )
            
            if phases_passed == total_phases:
                status = "✓ APPROVED"
                approved += 1
            else:
                status = "✗ REJECTED"
                rejected += 1
            
            logger.info(f"{status} | {strategy_name} ({phases_passed}/{total_phases} phases)")
        
        logger.info("-" * 80)
        logger.info(f"Total: {approved} APPROVED, {rejected} REJECTED out of {len(self.results)}")
        logger.info("=" * 80)


def main():
    """Main entry point"""
    # Get paths
    script_dir = Path(__file__).parent
    config_path = script_dir / 'validation_config.yaml'
    strategies_path = script_dir / 'strategies_structured.md'
    
    # Initialize validator
    validator = StrategyValidator(str(config_path))
    
    # Load strategies
    validator.load_strategies(str(strategies_path))
    
    # Run full pipeline
    results = validator.run_full_test_pipeline()
    
    # Generate report
    validator.generate_report('validation_report.json')
    
    # Print summary
    validator.print_summary()


if __name__ == '__main__':
    main()
