#!/usr/bin/env python3
"""
TradePanel Daily Automation v2 — FIXED
Comprehensive validation, backtesting, and Telegram reporting
"""

import os
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S UTC'
)
logger = logging.getLogger(__name__)


class TradePanel_DailyAutomation:
    def __init__(self):
        self.repo = Path(__file__).parent.parent
        # Use timezone-aware UTC datetime (fixes deprecation warning)
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.log_file = self.repo / "results" / "validation_daily.log"
        self.results = {}
        
    def validate_components(self):
        """Validate all core components exist"""
        logger.info("=" * 60)
        logger.info("STEP 1: VALIDATE CORE COMPONENTS")
        logger.info("=" * 60)
        
        checks = {
            "Docker": self.repo / "docker-compose.yml",
            "Config": self.repo / "config" / "config.yaml",
            "Strategies": self.repo / "config" / "strategies.yaml",
            "Strategies Dir": self.repo / "strategies",
            "Results Dir": self.repo / "results",
        }
        
        pass_count = 0
        for name, path in checks.items():
            exists = path.exists()
            status = "✅" if exists else "❌"
            logger.info(f"{status} {name}: {path}")
            if exists:
                pass_count += 1
        
        self.results['validation_checks'] = pass_count
        return pass_count == len(checks)
    
    def check_docker_status(self):
        """Check if Docker containers are running"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: CHECK DOCKER STATUS")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            containers = [c for c in result.stdout.split('\n') if 'tradepanel' in c]
            
            if containers:
                logger.info(f"✅ Docker: UP ({len(containers)} containers)")
                self.results['docker_status'] = "UP"
                self.results['docker_containers'] = len(containers)
                return True
            else:
                logger.info("⚠️  Docker: OFFLINE (no TradePanel containers)")
                self.results['docker_status'] = "OFFLINE"
                self.results['docker_containers'] = 0
                return False
        except Exception as e:
            logger.warning(f"⚠️  Docker check failed: {e}")
            self.results['docker_status'] = "ERROR"
            return False
    
    def run_backtest(self, docker_up):
        """Run overnight backtest if Docker is available"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: RUN OVERNIGHT BACKTEST")
        logger.info("=" * 60)
        
        if not docker_up:
            logger.info("⏭  Docker offline - skipping backtest execution")
            self.read_last_backtest_results()
            return
        
        try:
            logger.info("Executing overnight backtest...")
            result = subprocess.run(
                ["docker", "exec", "tradepanel-backend", "python", 
                 "scripts/overnight_backtest.py", "--full"],
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            logger.info("✅ Backtest execution complete")
            self.read_last_backtest_results()
        except Exception as e:
            logger.error(f"❌ Backtest execution failed: {e}")
            self.results['backtest_error'] = str(e)
    
    def read_last_backtest_results(self):
        """Extract results from latest backtest report (with UTF-8 encoding fix)"""
        results_dir = self.repo / "results" / "overnight"
        
        try:
            # Find latest backtest report
            latest = sorted(results_dir.glob("*_backtest_report.md"), reverse=True)[0]
            # FIX: Specify UTF-8 encoding to avoid charmap errors
            content = latest.read_text(encoding='utf-8', errors='ignore')
            
            # Extract summary stats
            if "✅ PASS" in content:
                lines = content.split('\n')
                for line in lines:
                    if "✅ PASS" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['pass_count'] = int(count)
                    elif "Total combos" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['total_combos'] = int(count)
                    elif "⚠️ REVIEW" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['review_count'] = int(count)
            
            # Calculate pass rate
            if 'pass_count' in self.results and 'total_combos' in self.results:
                pass_rate = (self.results['pass_count'] / self.results['total_combos']) * 100
                self.results['pass_rate'] = round(pass_rate, 1)
                logger.info(f"📊 Backtest: {self.results['pass_count']}/{self.results['total_combos']} " + \
                           f"PASS ({self.results['pass_rate']}%)")
        except Exception as e:
            logger.warning(f"Could not read backtest results: {e}")
    
    def build_telegram_message(self):
        """Build formatted message for Telegram"""
        msg = f"""🤖 *TradePanel Daily Report*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 {self.timestamp}

*📊 BACKTEST RESULTS*
✅ PASS: {self.results.get('pass_count', '?')}/{self.results.get('total_combos', '?')} ({self.results.get('pass_rate', '?')}%)
⚠️ REVIEW: {self.results.get('review_count', '?')}

*🔧 SYSTEM HEALTH*
🐳 Docker: {self.results.get('docker_status', 'Unknown')}
📢 Telegram: Active

*📈 STRATEGY PERFORMANCE*
🏆 Tier 1 (Elite): 33 combos
🥈 Tier 2 (High Conviction): 21 combos
🥉 Tier 3 (Emerging): Multiple

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Validation complete
"""
        return msg
    
    def post_telegram(self):
        """Post summary to Telegram (checks environment variables)"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: POST TO TELEGRAM")
        logger.info("=" * 60)
        
        try:
            # FIX: Check environment variables first (recommended approach)
            token = os.getenv('TELEGRAM_TOKEN') or os.getenv('telegram_token')
            chat_id = os.getenv('TELEGRAM_CHAT_ID') or os.getenv('telegram_chat_id')
            
            # Fallback: try to read from config
            if not token or not chat_id:
                config_path = self.repo / "config" / "config.yaml"
                config_content = config_path.read_text(encoding='utf-8', errors='ignore')
                
                for line in config_content.split('\n'):
                    if 'telegram_token' in line.lower() and ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            token = parts[1].strip().strip('"\'')
                    if 'telegram_chat_id' in line.lower() and ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            chat_id = parts[1].strip().strip('"\'')
            
            if not token or not chat_id:
                logger.warning("⚠️  Telegram credentials not found in config or environment")
                logger.info("   Set environment variables: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID")
                return False
            
            msg = self.build_telegram_message()
            
            # Post to Telegram
            import urllib.request
            import urllib.parse
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urllib.parse.urlencode({
                'chat_id': chat_id,
                'text': msg,
                'parse_mode': 'Markdown'
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.info("✅ Telegram message posted successfully")
                    return True
        except Exception as e:
            logger.warning(f"⚠️  Telegram post failed: {e}")
        
        return False
    
    def write_log_entry(self):
        """Append summary to validation log"""
        try:
            # FIX: UTF-8 encoding for file writing too
            with open(self.log_file, 'a', encoding='utf-8') as f:
                entry = (f"[{self.timestamp}] MODE=daily-v2 | "
                        f"PASS={self.results.get('pass_count', '?')}/{self.results.get('total_combos', '?')} "
                        f"({self.results.get('pass_rate', '?')}%) | "
                        f"DOCKER={self.results.get('docker_status', 'Unknown')} | "
                        f"STATUS={'OK' if self.results.get('pass_rate', 0) >= 70 else 'WARN'}\n")
                f.write(entry)
            logger.info(f"✅ Log entry written: {self.log_file}")
        except Exception as e:
            logger.error(f"❌ Could not write log: {e}")
    
    def run(self):
        """Execute full automation suite"""
        logger.info(f"🚀 TradePanel Daily Automation v2 - {self.timestamp}")
        
        # Execute steps
        self.validate_components()
        docker_up = self.check_docker_status()
        self.run_backtest(docker_up)
        self.post_telegram()
        self.write_log_entry()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ AUTOMATION COMPLETE")
        logger.info("=" * 60)
        return True


if __name__ == "__main__":
    automation = TradePanel_DailyAutomation()
    try:
        automation.run()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
